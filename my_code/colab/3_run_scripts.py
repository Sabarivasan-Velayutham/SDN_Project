import threading
import subprocess
import os

# read all the script files and save them to text files
client_directory = "client"
os.makedirs(client_directory, exist_ok=True)
# Function to run a bash script
def run_script(script_path):
    # Execute the script using subprocess.run()
    subprocess.run(["bash", script_path])

# Path to the scripts folder
scripts_folder = "scripts"

# Create a list to hold threads
threads = []

# Get the list of script files in the scripts folder
script_files = [os.path.join(scripts_folder, script) for script in os.listdir(scripts_folder) if script.endswith(".sh")]

# Create and start a thread for each script
for script_path in script_files:
    # Create a new thread for the script
    thread = threading.Thread(target=run_script, args=(script_path,))
    # Start the thread
    thread.start()
    # Append the thread to the list for tracking
    threads.append(thread)

# Wait for all threads to complete
for thread in threads:
    thread.join()

print("All scripts have finished execution.")