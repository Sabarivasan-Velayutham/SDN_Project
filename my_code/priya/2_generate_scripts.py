import threading
import subprocess
import os

data = ['10K','20K','30K','40K','50K','60K']

# Function to generate Bash script files based on processed data and bandwidth
def generate_scripts(data, output_directory):

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Iterate through each row and each value in the processed data
    for i in range(len(data)):
        # Calculate the script file index and name
        script_filename = f"script_{i+1}.sh"
        script_path = os.path.join(output_directory, script_filename)

        # Generate the content of the Bash script
        script_content = f"""#!/bin/bash

run_iperf_client() {{
    xterm -e "iperf -c 10.0.0.1 -p 500{i+1} -u -b {data[i]}"
}}

# Run iperf client in a separate xterm window
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
# Generate the script files based on the provided processed data
generate_scripts(data, output_directory)

