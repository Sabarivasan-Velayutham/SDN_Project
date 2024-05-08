
echo "Creating switch s1..."
sleep 1
sudo ovs-vsctl add-br s1

echo "Setting OpenFlow protocol version for bridge s1..."
sleep 1
sudo ovs-vsctl set Bridge s1 protocols=OpenFlow13

echo "Setting OVSDB manager to ptcp:6632..."
sleep 1
sudo ovs-vsctl set-manager ptcp:6632

echo "Setting ovsdb_addr for switch s1..."
sleep 1
sudo curl -X PUT -d '"tcp:127.0.0.1:6632"' http://localhost:8080/v1.0/conf/switches/0000000000000001/ovsdb_addr

echo "Defining bandwidth queues for port s1-eth1..."
sleep 1
sudo curl -X POST -d '{"port_name": "s1-eth1", "type": "linux-htb", "max_rate": "1000000", "queues": [{"max_rate": "50000"}]}' http://localhost:8080/qos/queue/0000000000000001

echo "Installing flow entries for UDP traffic..."
sleep 1
sudo curl -X POST -d '{"match": {"nw_dst": "10.0.0.1", "nw_proto": "UDP", "tp_dst": "5002"}, "actions":{"queue": "0"}}' http://localhost:8080/qos/rules/0000000000000001
sudo curl -X POST -d '{"match": {"nw_dst": "10.0.0.2", "nw_proto": "UDP", "tp_dst": "5002"}, "actions":{"queue": "0"}}' http://localhost:8080/qos/rules/0000000000000001
sudo curl -X POST -d '{"match": {"nw_dst": "10.0.0.3", "nw_proto": "UDP", "tp_dst": "5002"}, "actions":{"queue": "0"}}' http://localhost:8080/qos/rules/0000000000000001
