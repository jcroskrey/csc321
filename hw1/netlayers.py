import re
import platform

import requests
import toolz.curried as _
import larc
import larc.common as __

log = larc.logging.new_log(__name__)

ip_re = r'\d+\.\d+\.\d+\.\d+'
float_re = r'[+-]?(?:[0-9]*[.])?[0-9]+'

getoutput = larc.shell.getoutput(echo=False)

def lookup_mac(mac):
    return _.pipe(
        requests.get(f'http://macvendors.co/api/{mac}'),
        __.maybe_json(default={}),
        _.get('result', default={}),
        lambda d: {'mac': mac, 'info': d},
    )

@_.curry
def mac_conv(split_char, mac):
    return _.pipe(
        mac.split(split_char),
        _.map(lambda b: int(b, 16)),
        _.map(hex),
        _.map(lambda h: h[2:]),
        _.map(lambda h: h.zfill(2)),
        ':'.join,
        lookup_mac,
    )

win_mac_conv = mac_conv('-')
macos_mac_conv = mac_conv(':')

# ----------------------------------------------------------------------
# ARP
# ----------------------------------------------------------------------

arp_output_macos = _.partial(getoutput, 'arp -a')
arp_macos_re = re.compile(
    fr'^(?P<name>[?.\w-]*)\s+\((?P<ip>{ip_re})\) at (?P<mac>.*?) on .*$'
)

arp_output_win = _.partial(getoutput, 'arp -a')
arp_win_re = re.compile(
    fr'^\s+(?P<ip>{ip_re})\s+(?P<mac>.*?)\s+\w+\s*$'
)
 
def get_arp_data(arp_output, regex, mac_conv):
    return _.pipe(
        arp_output.splitlines(),
        _.map(regex.match),
        _.filter(None),
        _.map(__.call('groupdict')),
        larc.parallel.thread_map(
            lambda d: _.merge(d, mac_conv(d['mac'])),
            max_workers=5,
        ),
        tuple,
    )

def get_arp(arp_output_f, regex, mac_conv):
    def arp(*args):
        return _.pipe(
            arp_output_f(*args),
            lambda output: get_arp_data(output, regex, mac_conv),
        )
    return arp

get_arp_macos = get_arp(arp_output_macos, arp_macos_re, macos_mac_conv)
get_arp_win = get_arp(arp_output_win, arp_win_re, win_mac_conv)

# ----------------------------------------------------------------------
# ICMP ping
# ----------------------------------------------------------------------

@_.curry
def re_map(regex, map_d, content):
    match = regex.search(content)
    if match:
        d = match.groupdict()
        return _.merge(d, _.pipe(
            map_d,
            _.itemmap(__.vcall(lambda key, func: (
                key, func(d[key])
            ))),
        ))

    return {}

ping_re_macos = {
    'tick': re_map(re.compile(
        fr'\d+ bytes from (?P<ip>{ip_re}): icmp_seq=\d+ ttl=\d+'
        fr' time=(?P<ms>\d+(?:\.\d+)?) ms'
    ), {'ms': float}),
    'totals': re_map(re.compile(
        r'(?P<sent>\d+) packets transmitted,'
        r' (?P<received>\d+) packets received,'
        r' (?P<lost>\d+(?:\.\d+))% packet loss'
    ), {'sent': int, 'received': int, 'lost': float}),
    'stats': re_map(re.compile(
       fr'round-trip min/avg/max/stddev ='
       fr' (?P<min>{float_re})/'
       fr'(?P<avg>{float_re})/'
        fr'(?P<max>{float_re})/'
        fr'(?P<std>{float_re}) ms'
    ), {'min': float, 'avg': float, 'max': float, 'std': float}),
}

ping_re_win = {
    'stats': re_map(re.compile(
        r'    Minimum = (?P<min>\d+(?:\.\d+)?)ms,'
        r' Maximum = (?P<max>\d+(?:\.\d+)?)ms,'
        r' Average = (?P<avg>\d+(?:\.\d+)?)ms',
    ), {'min': float, 'max': float, 'avg': float}),
    'totals': re_map(re.compile(
        r'Packets: Sent = (?P<sent>\d+(?:\.\d+)?),'
        r' Received = (?P<received>\d+(?:\.\d+)?),'
        r' Lost = (?P<lost>\d+(?:\.\d+)?) (0% loss),'
    ), {'sent': float, 'received': float, 'lost': float}),
}

def ping_output_macos(host, n):
    options = f'-c {n}' if n else ''
    command = f'ping {options} {host}'
    log.info(f'Ping command: {command}')
    output = getoutput(command)
    return output

def ping_output_win(host, n):
    options = f'-n {n}' if n else ''
    command = f'ping {options} {host}'
    log.info(f'Ping command: {command}')
    output = getoutput(command)
    return output

def ping_stats_data(matches):
    if matches:
        stats = matches[0]
        return dict(map(lambda kv: (kv[0], float(kv[1])), stats.items()))
    return None

def get_ping_data(ping_output, regex, data, *a):
    lines = ping_output(*a).splitlines()
    matches = tuple(
        map(lambda m: m.groupdict(),
            filter(None, [regex.match(l) for l in lines]))
    )
    return data(matches)

get_ping_stats_macos = _.partial(
    get_ping_data, ping_output_macos, ping_re_macos['stats'], ping_stats_data
)

get_ping_stats_win = _.partial(
    get_ping_data, ping_output_win, ping_re_win['stats'], ping_stats_data
)
 
ping_output, ping_re = {
    'Windows': (ping_output_win, ping_re_win),
    'Darwin': (ping_output_macos, ping_re_macos),
}[platform.system()]

# ----------------------------------------------------------------------
# End-user functions
# ----------------------------------------------------------------------

get_arp = {
    'Windows': get_arp_win,
    'Darwin': get_arp_macos,
}[platform.system()]

def arp_table():
    log.info('Getting ARP info')
    arp_items = get_arp()
    names, ips, macs, companies = _.pipe(
        arp_items,
        _.map(lambda i: (i['name'], i['ip'], i['mac'],
                         i['info'].get('company', ''))),
        lambda items: zip(*items),
    )
    max_n, max_i, max_m, max_c = _.pipe(
        [names, ips, macs, companies],
        _.map(lambda l: max(l, key=len)),
        _.map(len),
        tuple,
    )
    header = [
        ['Name', 'IP', 'MAC', 'Company'],
        ['-' * max_n, '-' * max_i, '-' * max_m, '-' * max_c],
    ]
    _.pipe(
        _.concatv(header, zip(names, ips, macs, companies)),
        __.vmap(lambda n, i, m, c: (
            n.ljust(max_n), i.ljust(max_i), m.ljust(max_m), c.ljust(max_c)
        )),
        _.map('  '.join),
        '\n'.join,
        print,
    )


def get_ping(host, n):
    output = ping_output(host, n)

    return _.pipe(
        ping_re,
        _.itemmap(__.vcall(lambda key, func: (
            key, func(output)
        ))),
        _.valfilter(lambda v: v),
    )