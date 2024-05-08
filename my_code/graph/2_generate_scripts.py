import os

arr = [i for i in range(10, 70, 10)]

data = [
    [i for i in range(10, 70, 10)],
]
bandwidth = [
    ['L' for _ in range(len(arr))],
    # ['M' for _ in range(len(arr))],
    # ['H' for _ in range(len(arr))]
]


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
    xterm -e "iperf -c 10.0.0.1 -p {port} -u -b {value} | tee client/c{i}{j}.txt"
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
generate_scripts(data, bandwidth, output_directory)

