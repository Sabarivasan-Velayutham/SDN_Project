from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController, Host
from time import sleep


class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."
    def build(self):
        s1 = self.addSwitch('s1')

        h1 = self.addHost('h1', mac="00:00:00:00:11:11")
        h2 = self.addHost('h2', mac="00:00:00:00:11:12")
        h3 = self.addHost('h3', mac="00:00:00:00:11:13")
        h4 = self.addHost('h4', mac="00:00:00:00:11:14")

        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)
        self.addLink(h4, s1)


def run_servers(net):
    "Start iperf servers on h2, h3, and h4"
    h2, h3, h4 = net.get('h2', 'h3', 'h4')
    h2.cmd('xterm -e "iperf -s" &')
    h3.cmd('xterm -e "iperf -s" &')
    h4.cmd('xterm -e "iperf -s" &')


def run_client(host, server_ips, duration):
    "Start iperf client on h1 to connect to the servers"
    for server_ip in server_ips:
        host.cmd(f'xterm -e "iperf -c {server_ip} -t {duration}"')


if __name__ == '__main__':
    setLogLevel('info')
    topo = SingleSwitchTopo()
    c1 = RemoteController('c1', ip='127.0.0.1')
    net = Mininet(topo=topo, controller=c1)
    net.start()

    # Start iperf servers on h2, h3, and h4
    run_servers(net)

    # Get the host objects
    h1 = net.get('h1')

    # Run iperf clients on h1 to connect to h2, h3, and h4
    server_ips = ['10.0.0.2', '10.0.0.3', '10.0.0.4']
    duration = 15  # seconds
    run_client(h1, server_ips, duration)

    CLI(net)
    net.stop()
