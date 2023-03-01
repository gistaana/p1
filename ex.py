#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import CPULimitedHost, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
import sys

if len(sys.argv) != 3:
    print "Usage: python mininet.py linear n"
    sys.exit(1)

topo_type = sys.argv[1]
n = int(sys.argv[2])

if topo_type == 'linear':
    net = Mininet(host=CPULimitedHost, link=TCLink, switch=OVSSwitch)
    hosts = []
    switches = []

    # Create hosts
    for i in range(n):
        hosts.append(net.addHost('h{}'.format(i+1), cpu=.5/n))

    # Create switches
    for i in range(n-1):
        switches.append(net.addSwitch('s{}'.format(i+1)))

    # Connect hosts to switches
    for i in range(n-1):
        net.addLink(hosts[i], switches[i], bw=10, delay='5ms', loss=10, max_queue_size=1000)
        net.addLink(hosts[i+1], switches[i], bw=10, delay='5ms', loss=10, max_queue_size=1000)

    # Connect switches to each other
    for i in range(n-2):
        net.addLink(switches[i], switches[i+1], bw=10, delay='5ms', loss=10, max_queue_size=1000)

    net.start()
    CLI(net)
    net.stop()
else:
    print "Unknown topology type."
    sys.exit(1)

