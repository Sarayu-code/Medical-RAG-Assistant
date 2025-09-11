import json, os
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain.docstore.document import Document

EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL", "all-MiniLM-L6-v2")
STORE_DIR = os.getenv("STORE_DIR", "./store")

class Retriever:
    def __init__(self):
        self.emb = SentenceTransformer(EMBEDDINGS_MODEL)
        self.docs: List[Document] = []
        self.doc_texts: List[str] = []
        self.doc_embs = None  # numpy array [N, D]
        self._load()

    def _load_jsonl(self, path: str):
        items = []
        if not os.path.exists(path):
            return items
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    d = json.loads(line)
                    items.append(d)
                except Exception:
                    continue
        return items

    def _load(self):
        paths = [os.path.join(STORE_DIR, "medlineplus.jsonl"),
                 os.path.join(STORE_DIR, "cdc.jsonl")]
        items = []
        for p in paths:
            items.extend(self._load_jsonl(p))
        if not items:
            # Fallback single doc prompting user to ingest data
            self.docs = [Document(
                page_content="No medical corpus found. Run the ingestion scripts to populate ./store/*.jsonl.",
                metadata={"title": "Setup Required", "source": "system", "chunk_id": 0}
            )]
            self.doc_texts = [self.docs[0].page_content]
            self.doc_embs = self.emb.encode(self.doc_texts, normalize_embeddings=True)
            return

        for d in items:
            self.docs.append(Document(page_content=d.get("page_content", ""),
                                      metadata=d.get("metadata", {})))
            self.doc_texts.append(d.get("page_content", ""))

        self.doc_embs = self.emb.encode(self.doc_texts, normalize_embeddings=True)

    def reload(self):
        # simple rebuild
        self.__init__()

    def retrieve(self, query: str, k: int = 6) -> List[Document]:
        if self.doc_embs is None or not self.doc_texts:
            return []
        q = self.emb.encode([query], normalize_embeddings=True)[0]
        sims = np.dot(self.doc_embs, q)
        idx = np.argsort(-sims)[:k]
        return [self.docs[i] for i in idx]

retriever_singleton = Retriever()

def format_context(docs: List[Document]) -> str:
    parts = []
    for d in docs:
        m = d.metadata or {}
        title = m.get("title", "Source")
        src = m.get("source", "")
        parts.append(f"[{title}]({src}) :: {d.page_content}")
    return "\n\n---\n\n".join(parts)

def synthesize_answer(query: str, docs: List[Document], system_prompt: str) -> str:
    # Simple template-based answer that cites the top 2 sources.
    import textwrap
    citations = []
    for d in docs[:2]:
        m = d.metadata or {}
        title = m.get("title", "Source")
        src = m.get("source", "")
        if src:
            citations.append(f"[{title}]({src})")
        else:
            citations.append(title)
    body = (
        "Here’s what reputable sources say in general terms:\n"
        "- Summarize key symptoms/causes and when to seek care.\n"
        "- Provide simple, actionable self-care tips where appropriate.\n"
        "- Avoid diagnosis; encourage professional guidance if symptoms persist or worsen.\n"
    )
    src_line = "Sources: " + (", ".join(citations) if citations else "N/A")
    return textwrap.dedent(body) + src_line
