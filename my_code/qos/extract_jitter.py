import fileinput
import re

files = ['s1.txt', 's2.txt', 's3.txt', ] 

for file in files:
    with fileinput.input(files=file) as f:
        for line in f:
            # Search for the pattern "57.119 ms" | tee s3.txt
            match = re.search(r"(\d+\.\d+) ms", line)
            if match:
                extracted_value = match.group(1)
                print(f"Extracted value: {extracted_value} ms")
                break  # Stop reading after finding the first occurrence
        else:
            print("Not found")
