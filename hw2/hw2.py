import ipaddress
import netifaces as ni

# Q1 ===============================================================
"""
Home Network

['lo0',
 'gif0',
 'stf0',
 'en0',
 'en1',
 'en2',
 'en3',
 'en4',
 'bridge0',
 'p2p0',
 'awdl0',
 'llw0',
 'utun0',
 'utun1',
 'en5']

BU Network

['lo0',
 'gif0',
 'stf0',
 'en0',
 'en1',
 'en2',
 'en3',
 'en4',
 'bridge0',
 'p2p0',
 'awdl0',
 'llw0',
 'utun0',
 'utun1',
 'en5']
"""

def get_interfaces():
    """Return a list of all the interfaces on this host

    Args: None

    Returns: (list) List of interfaces for this host
    """
    return ni.interfaces()

# Q2 ================================================================
"""
Home Network

lo0 : None
gif0 : None
stf0 : None
en0 : dc:a9:04:87:47:91
en1 : 82:c9:aa:02:24:01
en2 : 82:c9:aa:02:24:00
en3 : 82:c9:aa:02:24:05
en4 : 82:c9:aa:02:24:04
bridge0 : 82:c9:aa:02:24:01
p2p0 : 0e:a9:04:87:47:91
awdl0 : 1e:42:fd:1b:4b:b4
llw0 : 1e:42:fd:1b:4b:b4
utun0 : None
utun1 : None
en5 : ac:de:48:00:11:22

Belhaven Network

lo0 : None
gif0 : None
stf0 : None
en0 : dc:a9:04:87:47:91
en1 : 82:c9:aa:02:24:01
en2 : 82:c9:aa:02:24:00
en3 : 82:c9:aa:02:24:05
en4 : 82:c9:aa:02:24:04
bridge0 : 82:c9:aa:02:24:01
p2p0 : 0e:a9:04:87:47:91
awdl0 : 1e:42:fd:1b:4b:b4
llw0 : 1e:42:fd:1b:4b:b4
utun0 : None
utun1 : None
en5 : ac:de:48:00:11:22
"""

def get_mac(interface:str):
    """For the given interface string, return the MAC address as a
    string

    Args:
      interface (str): String representation of the interface
          (e.g. "eth0" or "en0")

    Returns: (str) MAC address
    """
    intf = ni.ifaddresses(interface)

    if intf.get(ni.AF_LINK) == None:
        return None
    else:
        return intf.get(ni.AF_LINK)[0].get('addr')

# Q3 ================================================================
"""
Home Network

lo0 : {'v4': IPv4Address('127.0.0.1'), 'v6': IPv6Address('::1')}
gif0 : None
stf0 : None
en0 : {'v4': IPv4Address('10.0.0.32'), 'v6': IPv6Address('fe80::1c48:f22e:202e:3bb8')}
en1 : None
en2 : None
en3 : None
en4 : None
bridge0 : None
p2p0 : None
awdl0 : {'v4': None, 'v6': IPv6Address('fe80::1c42:fdff:fe1b:4bb4')}
llw0 : {'v4': None, 'v6': IPv6Address('fe80::1c42:fdff:fe1b:4bb4')}
utun0 : {'v4': None, 'v6': IPv6Address('fe80::7c37:7bfb:73e5:4fc0')}
utun1 : {'v4': None, 'v6': IPv6Address('fe80::830b:1591:d3c8:7e6')}
en5 : {'v4': None, 'v6': IPv6Address('fe80::aede:48ff:fe00:1122')}

Belhaven Network

lo0 : {'v4': IPv4Address('127.0.0.1'), 'v6': IPv6Address('::1')}
gif0 : {'v4': None, 'v6': None}
stf0 : {'v4': None, 'v6': None}
en0 : {'v4': IPv4Address('192.168.180.79'), 'v6': IPv6Address('fe80::1c48:f22e:202e:3bb8')}
en1 : {'v4': None, 'v6': None}
en2 : {'v4': None, 'v6': None}
en3 : {'v4': None, 'v6': None}
en4 : {'v4': None, 'v6': None}
bridge0 : {'v4': None, 'v6': None}
p2p0 : {'v4': None, 'v6': None}
awdl0 : {'v4': None, 'v6': IPv6Address('fe80::1c42:fdff:fe1b:4bb4')}
llw0 : {'v4': None, 'v6': IPv6Address('fe80::1c42:fdff:fe1b:4bb4')}
utun0 : {'v4': None, 'v6': IPv6Address('fe80::7c37:7bfb:73e5:4fc0')}
utun1 : {'v4': None, 'v6': IPv6Address('fe80::830b:1591:d3c8:7e6')}
en5 : {'v4': None, 'v6': IPv6Address('fe80::aede:48ff:fe00:1122')}
"""

def get_ips(interface: str):
    """For the given interface string, return a dictionary with
    the IPv4 and IPv6 address objects for that interface

    Args:
      interface (str): String representation of the interface
          (e.g. "eth0" or "en0")

    Returns: (dict) Dictionary with the following form
      {'v4': ipaddress.IPv4Address('192.168.65.48'),
       'v6': ipaddress.IPv6Address('fe80::14e1:8686:e720:57a')}
    """
    addrs = ni.ifaddresses(interface)

    if addrs.get(ni.AF_INET6) == None and addrs.get(ni.AF_INET) == None:

        return {'v4': None,
                'v6': None
                }
    elif addrs.get(ni.AF_INET6) == None and addrs.get(ni.AF_INET) != None:
        ipv4 = ipaddress.IPv4Address(addrs[ni.AF_INET][0]['addr'])

        return {'v4': ipv4,
                'v6': None
                }
    elif addrs.get(ni.AF_INET6) != None and addrs.get(ni.AF_INET) == None:
        ipv6_scope_id = addrs[ni.AF_INET6][0]['addr']
        ipv6_no_scope_id = ipv6_scope_id.split('%', 1)[0]
        ipv6 = ipaddress.IPv6Address(ipv6_no_scope_id)

        return {'v4': None,
                'v6': ipv6
                }
    else:
        ipv4 = ipaddress.IPv4Address(addrs[ni.AF_INET][0]['addr'])
        ipv6_scope_id = addrs[ni.AF_INET6][0]['addr']
        ipv6_no_scope_id = ipv6_scope_id.split('%', 1)[0]
        ipv6 = ipaddress.IPv6Address(ipv6_no_scope_id)

        return {'v4': ipv4, 
        		'v6': ipv6
        		}

# Q4 ================================================================
"""
Home Network

lo0 : {'v4': IPv4Address('255.0.0.0'), 'v6': IPv6Address('ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff')}
gif0 : None
stf0 : None
en0 : {'v4': IPv4Address('255.255.255.0'), 'v6': IPv6Address('ffff:ffff:ffff:ffff::')}
en1 : None
en2 : None
en3 : None
en4 : None
bridge0 : None
p2p0 : None
awdl0 : {'v4': None, 'v6': IPv6Address('ffff:ffff:ffff:ffff::')}
llw0 : {'v4': None, 'v6': IPv6Address('ffff:ffff:ffff:ffff::')}
utun0 : {'v4': None, 'v6': IPv6Address('ffff:ffff:ffff:ffff::')}
utun1 : {'v4': None, 'v6': IPv6Address('ffff:ffff:ffff:ffff::')}
en5 : {'v4': None, 'v6': IPv6Address('ffff:ffff:ffff:ffff::')}

Belhaven Network

lo0 : {'v4': IPv4Address('255.0.0.0'), 'v6': IPv6Address('ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff')}
gif0 : {'v4': None, 'v6': None}
stf0 : {'v4': None, 'v6': None}
en0 : {'v4': IPv4Address('255.255.240.0'), 'v6': IPv6Address('ffff:ffff:ffff:ffff::')}
en1 : {'v4': None, 'v6': None}
en2 : {'v4': None, 'v6': None}
en3 : {'v4': None, 'v6': None}
en4 : {'v4': None, 'v6': None}
bridge0 : {'v4': None, 'v6': None}
p2p0 : {'v4': None, 'v6': None}
awdl0 : {'v4': None, 'v6': IPv6Address('ffff:ffff:ffff:ffff::')}
llw0 : {'v4': None, 'v6': IPv6Address('ffff:ffff:ffff:ffff::')}
utun0 : {'v4': None, 'v6': IPv6Address('ffff:ffff:ffff:ffff::')}
utun1 : {'v4': None, 'v6': IPv6Address('ffff:ffff:ffff:ffff::')}
en5 : {'v4': None, 'v6': IPv6Address('ffff:ffff:ffff:ffff::')}
"""

def get_netmask(interface: str):
    """For the given interface string, return a dictionary with the
    IPv4 and IPv6 netmask objects (as IPv4/v6Address objects) for that
    interface

    Args:
      interface (str): String representation of the interface
          (e.g. "eth0" or "en0")

    Returns: (dict) Dictionary with the following form
      {'v4': ipaddress.IPv4Address('255.255.255.0'),
       'v6': ipaddress.IPv6Address('ffff:ffff:ffff:ffff::')}
    """
    addrs = ni.ifaddresses(interface)

    if addrs.get(ni.AF_INET6) == None and addrs.get(ni.AF_INET) == None:

        return {'v4': None,
                'v6': None
                }
    elif addrs.get(ni.AF_INET6) == None and addrs.get(ni.AF_INET) != None:
        ipv4 = ipaddress.IPv4Address(addrs[ni.AF_INET][0]['netmask'])

        return {'v4': ipv4,
                'v6': None
                }
    elif addrs.get(ni.AF_INET6) != None and addrs.get(ni.AF_INET) == None:
        ipv6_nm_slash = addrs[ni.AF_INET6][0]['netmask']
        ipv6_nm_no_slash = ipv6_nm_slash.split('/', 1)[0]
        ipv6 = ipaddress.IPv6Address(ipv6_nm_no_slash)

        return {'v4': None,
                'v6': ipv6
                }
    else:
        ipv4_nm = ipaddress.IPv4Address(addrs[ni.AF_INET][0]['netmask'])

        ipv6_nm_slash = addrs[ni.AF_INET6][0]['netmask']
        ipv6_nm_no_slash = ipv6_nm_slash.split('/', 1)[0]
        ipv6_nm = ipaddress.IPv6Address(ipv6_nm_no_slash)

        return {'v4': ipv4_nm, 
        		'v6': ipv6_nm
        		}

# Q5 ================================================================
"""
Home Network

lo0 : {'v4': IPv4Network('127.0.0.1/32'), 'v6': IPv6Network('::1/128')}
gif0 : None
stf0 : None
en0 : {'v4': IPv4Network('10.0.0.32/32'), 'v6': IPv6Network('fe80::1c48:f22e:202e:3bb8/128')}
en1 : None
en2 : None
en3 : None
en4 : None
bridge0 : None
p2p0 : None
awdl0 : {'v4': None, 'v6': IPv6Network('fe80::1c42:fdff:fe1b:4bb4/128')}
llw0 : {'v4': None, 'v6': IPv6Network('fe80::1c42:fdff:fe1b:4bb4/128')}
utun0 : {'v4': None, 'v6': IPv6Network('fe80::7c37:7bfb:73e5:4fc0/128')}
utun1 : {'v4': None, 'v6': IPv6Network('fe80::830b:1591:d3c8:7e6/128')}
en5 : {'v4': None, 'v6': IPv6Network('fe80::aede:48ff:fe00:1122/128')}

Belhaven Network

lo0 : {'v4': IPv4Network('127.0.0.1/32'), 'v6': IPv6Network('::1/128')}
gif0 : {'v4': None, 'v6': None}
stf0 : {'v4': None, 'v6': None}
en0 : {'v4': IPv4Network('192.168.180.79/32'), 'v6': IPv6Network('fe80::1c48:f22e:202e:3bb8/128')}
en1 : {'v4': None, 'v6': None}
en2 : {'v4': None, 'v6': None}
en3 : {'v4': None, 'v6': None}
en4 : {'v4': None, 'v6': None}
bridge0 : {'v4': None, 'v6': None}
p2p0 : {'v4': None, 'v6': None}
awdl0 : {'v4': None, 'v6': IPv6Network('fe80::1c42:fdff:fe1b:4bb4/128')}
llw0 : {'v4': None, 'v6': IPv6Network('fe80::1c42:fdff:fe1b:4bb4/128')}
utun0 : {'v4': None, 'v6': IPv6Network('fe80::7c37:7bfb:73e5:4fc0/128')}
utun1 : {'v4': None, 'v6': IPv6Network('fe80::830b:1591:d3c8:7e6/128')}
en5 : {'v4': None, 'v6': IPv6Network('fe80::aede:48ff:fe00:1122/128')}
"""

def get_network(interface: str):
    """For the given interface string, return a dictionary with
    the IPv4 and IPv6 network objects for that interface

    Args:
      interface (str): String representation of the interface
          (e.g. "eth0" or "en0")

    Returns: (dict) Dictionary with the following form
      {'v4': ipaddress.IPv4Network('192.168.65.0/24'),
       'v6': ipaddress.IPv6Network('fe80::/64')}
    """
    addrs = ni.ifaddresses(interface)

    if addrs.get(ni.AF_INET6) == None and addrs.get(ni.AF_INET) == None:

        return {'v4': None,
                'v6': None
                }
    elif addrs.get(ni.AF_INET6) == None and addrs.get(ni.AF_INET) != None:
        ipv4 = ipaddress.IPv4Network(addrs[ni.AF_INET][0]['addr'])

        return {'v4': ipv4,
                'v6': None
                }
    elif addrs.get(ni.AF_INET6) != None and addrs.get(ni.AF_INET) == None:
        ipv6_scope_id = addrs[ni.AF_INET6][0]['addr']
        ipv6_no_scope_id = ipv6_scope_id.split('%', 1)[0]
        ipv6 = ipaddress.IPv6Network(ipv6_no_scope_id)

        return {'v4': None,
                'v6': ipv6
                }
    else:
        ipv4 = ipaddress.IPv4Network(addrs[ni.AF_INET][0]['addr'])

        ipv6_scope_id = addrs[ni.AF_INET6][0]['addr']
        ipv6_no_scope_id = ipv6_scope_id.split('%', 1)[0]
        ipv6 = ipaddress.IPv6Network(ipv6_no_scope_id)

        return {'v4': ipv4, 
        		'v6': ipv6
        		}

    