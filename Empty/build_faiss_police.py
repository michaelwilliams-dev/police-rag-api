import os
import faiss
import json
import openai
import numpy as np

# CONFIG
openai.api_key = os.getenv("OPENAI_API_KEY")
data_dir = "data"
output_dir = "faiss_index"
os.makedirs(output_dir, exist_ok=True)

index_path = os.path.join(output_dir, "police_chunks.index")
metadata_path = os.path.join(output_dir, "police_metadata.json")
embedding_model = "text-embedding-3-small"

# Load chunk files
texts = []
metadata = []

for fname in os.listdir(data_dir):
    if fname.endswith(".txt"):
        fpath = os.path.join(data_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if len(content) >= 100:
                texts.append(content)
                metadata.append({"chunk_file": fname})

# Embedding
def get_embedding(text):
    text = text.replace("\n", " ")
    response = openai.Embedding.create(input=[text], model=embedding_model)
    return response["data"][0]["embedding"]

print(f"Embedding {len(texts)} chunks...")
embeddings = [get_embedding(t) for t in texts]

# Build FAISS index
dimension = len(embeddings[0])
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype("float32"))

# Save
faiss.write_index(index, index_path)
with open(metadata_path, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)

print(f"✅ Saved FAISS index to {index_path}")
print(f"✅ Saved metadata to {metadata_path}")
