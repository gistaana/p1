#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.node import CPULimitedHost
from mininet.log import setLogLevel
from mininet.link import TCLink
import sys


class singleT(t):
    def __init__(self,n):
        t.__init__(self,n)
        
        switch = self.addSwitch('s1')

        hosts = [self.addHost(f'h{i+1}',cpu=.5/n) for i in range(n)]

        for j in range(n):
            self.addLink(hosts[j], switch, bw=10, delay='5ms', loss=10, max_queue_size=1000)
            
class linearT(t):
    def __init__(self, n):
        t.__init__(self)
        
        s = [self.addSwitch(f's{i+1}') for i in range(n)]
        
        h = [self.addHost(f'h{j+1}', cpu=.5/n) for j in range(n)]
        
        for i in range(n):
            self.addLink(h[i], s[i], bw=10, delay='5ms', loss=10, max_queue_size=1000)
            if i < n-1:
                self.addLink(s[i], s[i+1], bw=10, delay='5ms', loss=10, max_queue_size=1000)
                 

class treeT(t):
    def __init__(self, depth):
        t.__init__(self, depth)
        
        a, b, s, h, sw = 1, 2, 2, 1, [self.addSwitch('s1')]
        
        for i in range((2**(depth+1)-1)//2):
            
            if i >= ((2**depth)//2)-1:
                sw.append(self.addHost(f'h{h_count}', cpu=.5/depth))
                sw.append(self.addHost(f'h{h_count+1}', cpu=.5/depth))
                h += 2
                
            else:
                sw.append(self.addSwitch(f's{s_count}'))
                sw.append(self.addSwitch(f's{s_count+1}'))
                s += 2
                
            self.addLink(sw[i],sw[a+i], bw=10, delay='5ms', loss=10, max_queue_size=1000)
            self.addLink(sw[i],sw[b+i], bw=10, delay='5ms', loss=10, max_queue_size=1000)
            a, b = b, b+1
            


class meshT(t):
    def __init__(self, n):
        t.__init__(self, n)
        
        s = [self.addSwitch(f's{i+1}') for i in range(n)]       
    
        h = [self.addHost(f'h{j+1}', cpu=.5/n) for j in range(n)]
        
        for i in range(n):
            for j in range(i+1, n):
                self.addLink(s[i], s[j], bw=10, delay='5ms', loss=10, max_queue_size=1000)
        
        for i in range(n):
            self.addLink(h[i], s[i], bw=10, delay='5ms', loss=10, max_queue_size=1000)


def runT():
    if sys.argv[1] == "single":
        t = singleT(int(sys.argv[2]))
    elif sys.argv[1] =="linear":
        t = linearT(int(sys.argv[2]))
    elif sys.argv[1] =="tree":
        t = treeT(int(sys.argv[2]))
    elif sys.argv[1] =="mesh":
        t = meshT(int(sys.argv[2]))
    else:
        print("Invalid input, try again");
        
    net = Mininet(topo, host = CPULimitedHost, link = TCLink)
    net.start()
    print("\n Dumping Connections = \n")
    dumpNodeConnections(net.hosts)
    print("\n Network Connectivity = \n")
    net.pingAll();
   
    for i in range(len(net.hosts):
            for j in range(i+1, len(net.hosts):
                net.iperf((net.get(f'h{i+1}'),net.get(f'h{j+1}')))
    print("\n Stopping Network \n")
    net.stop()

if __name__=='__main__':
    setLogLevel('info')
    runTest()

