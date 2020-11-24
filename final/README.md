
To get the pcap files I used this command while running the scripts on the correct nodes:
```
tcpdump -i eth0 -w filename.pcap
```

The mergecap command I used on these files was:
```
mergecap -w full-take.pcap wuserver.pcap wuclient.pcap taskvent.pcap taskwork.pcap tasksink.pcap
```

To parse out full-take.pcap, I separated packets based on port using:
```
tcpdump -n -r full-take.pcap port 7776 -w weather.pcap
```
and,
```
tcpdump -n -r full-take.pcap port 5557 or port 5558 -w task.pcap
```

