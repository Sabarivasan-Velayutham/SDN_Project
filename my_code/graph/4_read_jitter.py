import re
import os

# Function to extract jitter values from text files and save them directly to an output text file
def extract_jitter_and_save_to_txt(folder_path, output_file):
    jitter_pattern = re.compile(r"(\d+\.\d+) ms")
    
    def extract_number(filename):
        return int(filename[1:-4])

    # Get a list of all files in the folder and sort them based on the numerical part after 's'
    files = sorted([os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.txt')], key=lambda x: extract_number(os.path.basename(x)))
    
    # Open the output file for writing
    with open(output_file, 'w') as out_file:
        # Iterate through each file
        for file_path in files:
            # Read the file line by line to find the jitter value
            with open(file_path, 'r') as f:
                for line in f:
                    # Search for the jitter pattern in the current line
                    match = jitter_pattern.search(line)
                    if match:
                        # Extract the jitter value in milliseconds
                        jitter_value = match.group(1)
                        
                        print(file_path,jitter_value)
                        # Write the jitter value to the output text file as a new line
                        out_file.write(jitter_value + '\n')
                        
                        # Break the loop as we found the first occurrence of the jitter value in the current file
                        break
                        
# Define the folder path containing the input text files and the output file path
folder_path = 'client'  # Specify the folder containing the input text files
output_file_path = 'high_band_jitter.txt'  # Specify the output text file path

# Call the function to extract jitter values from text files and save them to the output text file
extract_jitter_and_save_to_txt(folder_path, output_file_path)

print(f"Jitter values saved to {output_file_path}.")
