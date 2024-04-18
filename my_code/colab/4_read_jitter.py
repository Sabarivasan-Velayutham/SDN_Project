import fileinput
import re
import os
import csv

# Function to extract jitter values and store them in a 2D array
def extract_jitter(folder_path, num_rows, num_cols):
    # Create a 2D array to store the extracted jitter values
    jitter_array = [[None for _ in range(num_cols)] for _ in range(num_rows)]
    
    # Define the regex pattern to match the jitter values
    interval_pattern = re.compile(r"3\.0- 4\.0 sec") #3.0- 4.0 sec
    jitter_pattern = re.compile(r"(\d+\.\d+) ms")
    
    # Get a list of all files in the specified folder
    files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.txt')]
    
    # Iterate through each file
    for file_path in files:
        # Extract the filename (e.g., 's1.txt') and index
        filename = os.path.basename(file_path)
        if filename.startswith('s') and filename.endswith('.txt'):
            # Extract the index from the filename
            file_index = filename[1:-4]  # Get the index part between 's' and '.txt'
            
            # Calculate the row and column indices
            row = int(file_index[0])
            col = int(file_index[1])
            
            # Read the file to find the jitter value
            with fileinput.input(files=file_path) as f:
                for line in f:
                    if interval_pattern.search(line):
                        # Extract the jitter value using regex pattern
                        match = jitter_pattern.search(line)
                        if match:
                            # Extracted jitter value in milliseconds
                            extracted_value = float(match.group(1))
                            
                            # Store the extracted value in the 2D array
                            jitter_array[row][col] = extracted_value
                            
                            # Break the loop as we found the first occurrence of jitter value
                            break
                    else:
                        # If no jitter value found, you can handle the case here (e.g., print a message)
                        print(f"No jitter value found in file: {filename}")
    
    # Return the 2D array containing jitter values
    return jitter_array


# Function to save a 2D array to a CSV file
def save_to_csv(array, csv_file):
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in array:
            writer.writerow(row)


folder_path = 'server' 

# Define the number of rows and columns in the 2D array
num_rows = 5  
num_cols = 7

# Call the function to extract jitter values and store them in a 2D array
jitter_array = extract_jitter(folder_path, num_rows, num_cols)

# Print the 2D array
for row in jitter_array:
    print(row)

# Define the CSV file path where the 2D array will be saved
csv_file_path = 'jitter_values.csv'
save_to_csv(jitter_array, csv_file_path)
print(f"Jitter values saved to {csv_file_path}.")