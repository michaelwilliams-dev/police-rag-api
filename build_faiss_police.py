import os
import faiss
import json
import openai
import numpy as np
import csv
from tqdm import tqdm
from openai import OpenAI
import unicodedata

# === Embedding function (OpenAI v1+, unicode-safe) ===
def get_embedding(text, model="text-embedding-3-small"):
    client = OpenAI()
    # Normalize and sanitize text
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("utf-8", errors="ignore").decode("utf-8")
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

# === Paths and config ===
openai.api_key = os.getenv("OPENAI_API_KEY")
input_dir = os.path.expanduser('~/Documents/police_chunking/data')
log_path = os.path.expanduser('~/Documents/police_chunking/chunk_log.csv')
output_dir = os.path.expanduser('~/Documents/police_chunking/faiss_index')
os.makedirs(output_dir, exist_ok=True)

index_path = os.path.join(output_dir, 'police_chunks.index')
metadata_path = os.path.join(output_dir, 'police_metadata.json')
error_log_path = os.path.join(output_dir, 'embedding_errors.log')
embedding_model = "text-embedding-3-small"

# === Load chunked files and metadata ===
texts = []
metadata = []

print("📥 Reading chunk files and metadata...")

with open(log_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        chunk_path = os.path.join(os.path.expanduser('~/Documents/police_chunking'), row['chunk_path'])
        if not os.path.exists(chunk_path):
            continue
        with open(chunk_path, 'r', encoding='utf-8') as chunk_file:
            content = chunk_file.read().strip()
            if len(content.split()) >= 100:
                texts.append(content)
                metadata.append({
                    "source_file": row["original_filename"],
                    "chunk_file": row["chunk_filename"],
                    "chunk_number": int(row["chunk_number"]),
                    "word_count": int(row["word_count"]),
                    "chunk_path": row["chunk_path"]
                })

print(f"🧠 Generating {len(texts)} embeddings...")

# === Generate embeddings with safe error logging ===
embeddings = []
with open(error_log_path, 'w', encoding='utf-8') as errlog:
    for i, text in enumerate(tqdm(texts)):
        try:
            emb = get_embedding(text, model=embedding_model)
            embeddings.append(emb)
        except Exception as e:
            # Log the full error to file
            errlog.write(f"Chunk {i} failed: {e}\n")
            # Print only safe summary
            print(f"❌ Error on chunk {i}: encoding issue or API failure")
            embeddings.append([0.0] * 1536)

# === Build FAISS index ===
dimension = len(embeddings[0])
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype("float32"))

faiss.write_index(index, index_path)
with open(metadata_path, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)

print(f"\n✅ FAISS index saved to: {index_path}")
print(f"📄 Metadata saved to: {metadata_path}")
print(f"🛠 Errors (if any) logged to: {error_log_path}")