import wikipedia
from tqdm import tqdm
from .config import SCRAPE_LIMIT, CHUNK_SIZE, CHUNK_LIMIT
from .vector_store import VectorStore
from sentence_transformers import SentenceTransformer
def scrape_topic(topic, limit=SCRAPE_LIMIT):
    titles = wikipedia.search(topic, results=limit)
    texts = []
    for t in titles:
        try:
            pg = wikipedia.page(t, auto_suggest=False)
            texts.append({"title": t, "text": pg.content})
        except Exception:
            continue
    return texts
def chunk_text(text, chunk_size=CHUNK_SIZE):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
def ingest_topic(topic):
    vs = VectorStore(topic)
    if vs.index is not None:
        return {"status":"cached","topic":topic,"chunks":len(vs.meta)}
    docs = scrape_topic(topic)
    if not docs:
        return {"status":"no_data","topic":topic}
    all_chunks, meta = [], []
    embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    for doc in docs:
        chunks = chunk_text(doc['text'])[:CHUNK_LIMIT]
        all_chunks.extend(chunks)
        meta.extend([{'text':c,'source':doc['title']} for c in chunks])
    embeddings = embedder.encode(all_chunks, convert_to_numpy=True)
    vs.build(embeddings, meta)
    return {"status":"ingested","topic":topic,"chunks":len(all_chunks)}
