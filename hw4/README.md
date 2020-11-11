#### To get names.tsv:
I ran the command: cat domains.tsv | tail -n +2 | cut -f2 > names.tsv

#### To get ips.tsv:
I ran the command: cat domains.tsv | tail -n +2 | cut -f2 | while read hostname; do host ${hostname} | grep "has address" | cut -d ' ' -f 4; done > ips.tsv

#### To get reversemapping.tsv:
I ran the command: cat domains.tsv | tail -n +2 | cut -f2 | while read hostname; do echo; echo; echo $hostname; host ${hostname} | grep "has address" | cut -d ' ' -f 4 | while read ip; do host $ip; done | grep "domain name pointer" | awk '{ print $5 }'; done > reversemapping.tsv

