import threading
import subprocess

# Function to run a bash script
def run_script(script_path):
    # Execute the script using subprocess.run()
    subprocess.run(["bash", script_path])

# Paths to the bash scripts you want to execute
script1 = "iperf1.sh"
script2 = "iperf2.sh"
script3 = "iperf3.sh"

# Create a list to hold threads
threads = []

# Create and start a thread for each script
for script in [script1, script2, script3]:
    # Create a new thread for the script
    thread = threading.Thread(target=run_script, args=(script,))
    # Start the thread
    thread.start()
    # Append the thread to the list for tracking
    threads.append(thread)

# Wait for all threads to complete
for thread in threads:
    thread.join()

print("All scripts have finished execution.")
