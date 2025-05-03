import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer
import file_parser as fp

class CodeRetriever:
    def __init__(self, index_path="data/code_index.faiss", snippets_path="data/snippets.json"):
        self.embedder = SentenceTransformer('BAAI/bge-small-en')  # You can change model here
        self.index_path = index_path
        self.snippets_path = snippets_path
        self.index = None
        self.snippets = []
        self.MIN_SCORE_THRESHOLD = 5.0  # adjust based on experiments
        self.PREFERRED_LANGUAGE = "java"  # or None if you want any language
        self.load_index_and_snippets()

    def load_index_and_snippets(self):
        # Load snippets
        with open(self.snippets_path, "r") as f:
            self.snippets = json.load(f)
        
        # Load FAISS index
        self.index = faiss.read_index(self.index_path)
        print(f"[Retriever] Loaded {len(self.snippets)} snippets.")
        print(f"[Retriever] FAISS index size: {self.index.ntotal}")

    def search(self, query, k=20):
        if self.index is None:
            return [{"error": "Index not loaded."}]

        # Embed the query
        query_vec = self.embedder.encode([query], convert_to_numpy=True)

        # Search
        distances, indices = self.index.search(query_vec, k)

        results = []
        for idx, score in zip(indices[0], distances[0]):
            if idx < len(self.snippets):
                snippet = self.snippets[idx]
                if score >= self.MIN_SCORE_THRESHOLD:
                    continue  # Skip low-quality results

                if self.PREFERRED_LANGUAGE:
                    snippet_language = snippet.get("language", "").lower()
                    if snippet_language != self.PREFERRED_LANGUAGE.lower():
                        continue  # Skip if not preferred language

                results.append({
                    "code": snippet.get("code", ""),
                    "link": snippet.get("repo_name", "No Repo Name Available"),
                    "score": float(score)
                })
        return results