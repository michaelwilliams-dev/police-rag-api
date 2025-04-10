import os
import csv

def split_text_file(input_file_path, output_dir, log_writer, chunk_size=500, overlap=50):
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file_path, 'r', encoding='latin-1', errors='ignore') as input_file:
        content = input_file.read()
        words = content.split()

    file_name = os.path.basename(input_file_path)
    base_name, extension = os.path.splitext(file_name)

    chunk_number = 1
    for i in range(0, len(words), chunk_size - overlap):
        chunk_words = words[i:i + chunk_size]
        if not chunk_words:
            break

        chunk_text = ' '.join(chunk_words)
        chunk_file_name = f"{base_name}_chunk_{chunk_number}{extension}"
        chunk_file_path = os.path.join(output_dir, chunk_file_name)

        with open(chunk_file_path, 'w', encoding='utf-8') as chunk_file:
            chunk_file.write(chunk_text)

        log_writer.writerow([
            file_name,
            chunk_file_name,
            chunk_number,
            len(chunk_words),
            os.path.relpath(chunk_file_path, start=os.path.expanduser('~/Documents/police_chunking'))
        ])

        chunk_number += 1

# ---- Main Script ---- #

input_directory = os.path.expanduser('~/Documents/police_chunking/police_text')
output_directory = os.path.expanduser('~/Documents/police_chunking/data')
log_path = os.path.expanduser('~/Documents/police_chunking/chunk_log.csv')

chunk_size = 500
overlap = 50

# Ensure clean output
for f in os.listdir(output_directory):
    if f.endswith('.txt'):
        os.remove(os.path.join(output_directory, f))

# Create log
with open(log_path, 'w', newline='', encoding='utf-8') as log_file:
    log_writer = csv.writer(log_file)
    log_writer.writerow(["original_filename", "chunk_filename", "chunk_number", "word_count", "chunk_path"])

    for file_name in os.listdir(input_directory):
        if file_name.endswith('.txt'):
            input_path = os.path.join(input_directory, file_name)
            split_text_file(input_path, output_directory, log_writer, chunk_size, overlap)

print("✅ All text files chunked with overlap and logged to chunk_log.csv.")