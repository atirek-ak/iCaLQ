import os

def getNumbersFromCsvFiles(directory):
    # List to store the numbers
    numbers = []
    
    # Iterate over all files in the given directory
    for filename in os.listdir(directory):
        # Check if the file ends with .csv
        if filename.endswith('.csv'):
            # Remove the .csv extension and convert to an integer
            number = int(filename[:-4])
            # Add the number to the list
            numbers.append(number)
    
    return numbers

def getImmediateSubdirectories(directory):
    # List to store the names of subdirectories
    subdirectories = []
    
    # Iterate over all entries in the given directory
    for entry in os.listdir(directory):
        # Create the full path
        full_path = os.path.join(directory, entry)
        # Check if the entry is a directory
        if os.path.isdir(full_path):
            # Add the directory name to the list
            subdirectories.append(int(entry))
    
    return subdirectories

def transposeMatrix(matrix):
    # Use zip to transpose the rows to columns and convert them to lists
    columns = [list(column) for column in zip(*matrix)]
    return columns