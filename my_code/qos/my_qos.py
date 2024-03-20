from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController, Host
import time
import subprocess


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


def set_openflow_settings():
    # Run OpenFlow setting commands
    print("Setting OpenFlow settings...")
    commands = [
        "ovs-vsctl set Bridge s1 protocols=OpenFlow13",
        "ovs-vsctl set-manager ptcp:6632"
    ]
    for cmd in commands:
        print(f"Executing: {cmd}")
        subprocess.run(["mn", "exec", "sh", "-c", cmd])

def set_ovsdb_addr():
    # Set ovsdb_addr
    print("Setting ovsdb_addr...")
    cmd = 'curl -X PUT -d "tcp:127.0.0.1:6632" http://localhost:8080/v1.0/conf/switches/0000000000000001/ovsdb_addr'
    subprocess.run(["mn", "exec", "sh", "-c", cmd], stdout=subprocess.PIPE)

def define_bandwidth_queues():
    # Define bandwidth of queues
    print("Defining bandwidth of queues...")
    queues_data = [
        {
            "port_name": "s1-eth1",
            "type": "linux-htb",
            "max_rate": "1000000",
            "queues": [
                {"min_rate": "800000", "max_rate": "1000000"},
                {"min_rate": "400000", "max_rate": "800000"},
                {"max_rate": "400000"}
            ]
        },
        {
            "port_name": "s1-eth1",
            "type": "linux-htb",
            "max_rate": "1000000",
            "queues": [
                {"max_rate": "500000"},
                {"min_rate": "800000"}
            ]
        }
    ]
    for data in queues_data:
        subprocess.run(["mn", "exec", "curl", "-X", "POST", "-d", f'\'{data}\'', "http://localhost:8080/qos/queue/s1"])

def install_flow_entries():
    # Install flow entries
    print("Installing flow entries...")
    rules_data = [
        {"match": {"nw_dst": "10.0.0.2", "nw_proto": "UDP", "tp_dst": "5001"}, "actions": {"queue": "1"}},
        {"match": {"nw_dst": "10.0.0.3", "nw_proto": "UDP", "tp_dst": "5002"}, "actions": {"queue": "2"}},
        {"match": {"nw_dst": "10.0.0.4", "nw_proto": "UDP", "tp_dst": "5003"}, "actions": {"queue": "3"}}
    ]
    for data in rules_data:
        subprocess.run(["mn", "exec", "curl", "-X", "POST", "-d", f'\'{data}\'', "http://localhost:8080/qos/rules/s1"])

def check_switch_contents():
    # Check contents of switch
    print("Checking contents of switch...")
    subprocess.run(["mn", "exec", "curl", "-X", "GET", "http://localhost:8080/qos/rules/s1"], stdout=subprocess.PIPE)


if __name__ == '__main__':
    setLogLevel('info')
    topo = SingleSwitchTopo()
    c1 = RemoteController('c1', ip='127.0.0.1')
    net = Mininet(topo=topo, controller=c1)
    net.start()

    set_openflow_settings()
    set_ovsdb_addr()
    define_bandwidth_queues()
    install_flow_entries()
    check_switch_contents()
    CLI(net)
    net.stop()