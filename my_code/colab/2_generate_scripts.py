import threading
import subprocess
import os

def process_data(input_data):
    processed_data = []
    for row in input_data:
        processed_row = []
        for value in row:
            result = ((value/15) * 1470) / 1024
            if result < 1024:
                processed_row.append(f"{result:.2f}K")
            else:
                result /= 1024
                processed_row.append(f"{result:.2f}M")
        processed_data.append(processed_row)
    return processed_data

original_data = [
    [6, 3360, 4654, 29, 13990, 6, 13],
    [76, 3263, 11364, 2, 10070, 76, 29],
    [77, 2531, 8958, 0, 3415, 77, 26911],
    [9, 3258, 22211, 1, 2533, 9, 144],
    [11, 3274, 5644, 6, 6775, 11, 181]
]

bandwidth = [
    ['L', 'H', 'H', 'M', 'H', 'L', 'M'],
    ['M', 'H', 'H', 'L', 'H', 'M', 'L'],
    ['M', 'M', 'H', 'L', 'H', 'L', 'H'],
    ['L', 'H', 'H', 'L', 'M', 'M', 'M'],
    ['M', 'H', 'H', 'L', 'H', 'L', 'M']
]

processed_data = process_data(original_data)

# Function to generate Bash script files based on processed data and bandwidth
def generate_scripts(processed_data, bandwidth, output_directory):
    # Define the port mapping based on bandwidth type
    port_mapping = {'H': 5004, 'M': 5003, 'L': 5002}

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Iterate through each row and each value in the data and bandwidth arrays
    for i, (row_data, row_bandwidth) in enumerate(zip(processed_data, bandwidth)):
        for j, (value, bw_type) in enumerate(zip(row_data, row_bandwidth)):
            # Calculate the script file index and name
            # script_index = i * len(row_data) + j
            script_filename = f"s{i}{j}.sh"
            script_path = os.path.join(output_directory, script_filename)

            # Determine the port based on bandwidth type
            port = port_mapping[bw_type]

            # Generate the content of the Bash script
            script_content = f"""#!/bin/bash

# Function to run iperf server in xterm
run_iperf_server() {{
    xterm -e "iperf -s -u -i 1 -p {port} | tee server/s{i}{j}.txt"
}}

# Function to run iperf client in xterm
run_iperf_client() {{
    xterm -e "iperf -c 10.0.0.1 -p {port} -u -b {value}"
}}

# Run iperf server in a separate xterm window
run_iperf_server &
run_iperf_client &
"""

            # Write the script content to the file
            with open(script_path, "w") as script_file:
                script_file.write(script_content)

            # Make the script file executable
            os.chmod(script_path, 0o755)

    print(f"Script files have been generated in the '{output_directory}' directory.")


# Define the output directory for the scripts
output_directory = "scripts"
# Generate the script files based on the provided processed data and bandwidth
generate_scripts(processed_data, bandwidth, output_directory)

