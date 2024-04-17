#!/bin/bash

# Function to run iperf server in xterm
run_iperf_server() {
    xterm -e "iperf -s -u -i 1 -p 5002"
}

# Function to run iperf client in xterm
run_iperf_client() {
    xterm -e "iperf -c 10.0.0.1 -p 5002 -u -b 0.19K | tee client/s13.txt"
}

# Run iperf server in a separate xterm window
run_iperf_server &
run_iperf_client &
