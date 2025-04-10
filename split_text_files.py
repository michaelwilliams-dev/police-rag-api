import os

def split_text_file(input_file_path, output_dir, lines_per_chunk=500):
    """
    Splits a text file into smaller files, each containing a specified number of lines.

    :param input_file_path: Path to the input text file.
    :param output_dir: Directory where the chunk files will be saved.
    :param lines_per_chunk: Number of lines each chunk should contain.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        file_name = os.path.basename(input_file_path)
        base_name, extension = os.path.splitext(file_name)

        chunk_number = 1
        while True:
            # Read the specified number of lines
            lines = [input_file.readline() for _ in range(lines_per_chunk)]
            # Remove any empty lines at the end of the file
            lines = [line for line in lines if line]
            if not lines:
                break
            # Define the chunk file name
            chunk_file_name = f"{base_name}_chunk_{chunk_number}{extension}"
            chunk_file_path = os.path.join(output_dir, chunk_file_name)
            # Write the chunk to a new file
            with open(chunk_file_path, 'w', encoding='utf-8') as chunk_file:
                chunk_file.writelines(lines)
            chunk_number += 1

# Define the input and output directories
input_directory = os.path.expanduser('~/Documents/police_chunking/police_text')
output_directory = os.path.expanduser('~/Documents/police_chunking/data')

# Number of lines per chunk
lines_per_chunk = 500  # Adjust as needed

# Iterate over all text files in the input directory
for file_name in os.listdir(input_directory):
    if file_name.endswith('.txt'):
        input_file_path = os.path.join(input_directory, file_name)
        split_text_file(input_file_path, output_directory, lines_per_chunk)