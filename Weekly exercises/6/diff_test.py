import difflib

# Define the paths to the two files you want to compare
file1_path = 'test.txt'
file2_path = 'test_equal.txt'

# Read the contents of the two files
with open(file1_path, 'r') as file1:
    file1_content = file1.readlines()

with open(file2_path, 'r') as file2:
    file2_content = file2.readlines()

# Use difflib to generate the differences between the two files
differ = difflib.Differ()
differences = list(differ.compare(file1_content, file2_content))

# Print the differences
for line in differences:
    print(line)
