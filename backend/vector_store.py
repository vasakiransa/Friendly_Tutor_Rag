import faiss, json, numpy as np
from pathlib import Path
from .config import VECTOR_DIR
def idx_path(topic): return VECTOR_DIR / f"{topic}_faiss.bin"
def meta_path(topic): return VECTOR_DIR / f"{topic}_meta.json"
class VectorStore:
    def __init__(self, topic):
        self.topic = topic
        self.index = None
        self.meta = []
        self.idx = idx_path(topic)
        self.meta_file = meta_path(topic)
        if self.idx.exists() and self.meta_file.exists():
            self.load()
    def build(self, embeddings: np.ndarray, metadatas: list):
        embeddings = np.array(embeddings, dtype="float32")
        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)
        faiss.normalize_L2(embeddings)
        d = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(d)
        self.index.add(embeddings)
        self.meta = metadatas
        self.save()
    def add(self, embeddings: np.ndarray, metadatas: list):
        embeddings = np.array(embeddings, dtype="float32")
        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)
        faiss.normalize_L2(embeddings)
        if self.index is None:
            self.build(embeddings, metadatas)
            return
        self.index.add(embeddings)
        self.meta.extend(metadatas)
        self.save()
    def search(self, query_emb, top_k=5):
        import numpy as np
        q = np.atleast_2d(np.array(query_emb, dtype="float32"))
        faiss.normalize_L2(q)
        D, I = self.index.search(q, top_k)
        results = []
        for idx, score in zip(I[0], D[0]):
            if 0 <= idx < len(self.meta):
                results.append({"score": float(score), "text": self.meta[idx]["text"], "source": self.meta[idx].get("source")})
        return results
    def save(self):
        faiss.write_index(self.index, str(self.idx))
        with open(self.meta_file, "w", encoding="utf-8") as f:
            json.dump(self.meta, f, ensure_ascii=False, indent=2)
    def load(self):
        self.index = faiss.read_index(str(self.idx))
        with open(self.meta_file, "r", encoding="utf-8") as f:
            self.meta = json.load(f)
