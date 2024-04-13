
import os
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController, Host
from time import sleep
from subprocess import PIPE, Popen


class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."
    def build(self):
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        h1 = self.addHost('h1', mac="00:00:00:00:11:11", ip="192.168.1.1/24")
        h2 = self.addHost('h2', mac="00:00:00:00:11:12", ip="192.168.1.2/24")

        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(s1, s2)


def run_receiver(host):
    # Execute ITGRecv command in xterm shell
    receiver_cmd = 'xterm -e ITGRecv -l /tmp/receiverr.log &'
    host.cmd(receiver_cmd)

    # sleep(2)
    # mn_cli_pid = os.getpid()
    # # Use wmctrl to bring Mininet CLI window to front
    # wmctrl_cmd = ['wmctrl', '-ia', str(mn_cli_pid)]
    # Popen(wmctrl_cmd, stdout=PIPE, stderr=PIPE)  


def run_sender(host):
    # Execute ITGSend command in Mininet shell
    sender_cmd = 'ITGSend -T TCP -a h2 -c 1000 -O 50 -t 10000'
    host.cmd(sender_cmd)


def run_decoder(host):
    # Execute ITGDec command in xterm shell
    decoder_cmd = 'xterm -e sh -c "cd /tmp && ITGDec /tmp/receiverr.log"'
    host.cmd(decoder_cmd)


if __name__ == '__main__':
    setLogLevel('info')
    topo = SingleSwitchTopo()
    c1 = RemoteController('c1', ip='127.0.0.1')
    net = Mininet(topo=topo, controller=c1)
    net.start()

    # Get the host objects
    h1 = net.get('h1')
    h2 = net.get('h2')

    run_receiver(h2)
    sleep(2)
    run_sender(h1)
    
    # Start the decoder in xterm shell
    # run_decoder(h2)

    CLI(net)
    net.stop()
