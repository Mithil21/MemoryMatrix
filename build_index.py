# build_index.py

import json
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

SNIPPET_FILE = "data/snippets.json"
INDEX_FILE = "data/code_index.faiss"
METADATA_FILE = "data/code_metadata.json"

def build_faiss_index():
    if not os.path.exists(SNIPPET_FILE):
        print(f"❌ File not found: {SNIPPET_FILE}")
        return

    with open(SNIPPET_FILE, "r", encoding="utf-8") as f:
        snippets = json.load(f)

    if not snippets:
        print("❌ No snippets to index.")
        return

    print("🔄 Loading embedding model...")
    model = SentenceTransformer("BAAI/bge-small-en")

    print("🔄 Creating embeddings...")
    texts = [
        f"{snippet.get('tags', [])} | {snippet['language']} code:\n{snippet['code']}"
        for snippet in snippets
    ]
    embeddings = model.encode(texts, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")

    print("🧠 Building FAISS index...")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, INDEX_FILE)
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(snippets, f, indent=2)

    print(f"✅ Index written to {INDEX_FILE}")
    print(f"✅ Metadata written to {METADATA_FILE}")

if __name__ == "__main__":
    build_faiss_index()