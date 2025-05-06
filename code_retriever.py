import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer
import file_parser as fp
from code_explainer import CodeExplainer  # Add explainer

class CodeRetriever:
    def __init__(self, index_path="data/code_index.faiss", snippets_path="data/snippets.json"):
        self.embedder = SentenceTransformer('BAAI/bge-small-en')  # Embedding model
        self.index_path = index_path
        self.snippets_path = snippets_path
        self.index = None
        self.PREFERRED_LANGUAGE = None
        self.snippets = []
        self.MIN_SCORE_THRESHOLD = 1.5  # adjust based on experiments
        self.load_index_and_snippets()
        self.explainer = CodeExplainer()  # Initialize explainer

    def load_index_and_snippets(self):
        with open(self.snippets_path, "r") as f:
            self.snippets = json.load(f)
        self.index = faiss.read_index(self.index_path)
        print(f"[Retriever] Loaded {len(self.snippets)} snippets.")
        print(f"[Retriever] FAISS index size: {self.index.ntotal}")

    def search(self, query, k=20):
        if self.index is None:
            return [{"error": "Index not loaded."}]

        query_vec = self.embedder.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_vec, k)

        results = []
        for idx, score in zip(indices[0], distances[0]):
            if idx < len(self.snippets):
                snippet = self.snippets[idx]
                if score >= self.MIN_SCORE_THRESHOLD:
                    continue

                code = snippet.get("code", "")
                explanation = self.explainer.explain(code)

                results.append({
                "code": code,
                "link": snippet.get("repo_name", "No Repo Name Available"),
                "language": snippet.get("language", "Unknown"),  # <- Add this
                "score": float(score),
                "explanation": explanation
            })

        return results