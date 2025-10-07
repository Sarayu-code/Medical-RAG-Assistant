import re, hashlib
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter

def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    # Remove nav/aside/script/style
    for tag in soup(["script", "style", "nav", "aside", "footer", "header"]):
        tag.decompose()
    text = soup.get_text("\n", strip=True)
    # Normalize whitespace
    return re.sub(r"\n{2,}", "\n", text).strip()

def chunk_text(text: str, source: str, title: str, chunk_size=800, chunk_overlap=120):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_text(text)
    docs = []
    for i, c in enumerate(chunks):
        uid = hashlib.md5(f"{source}-{i}".encode()).hexdigest()
        docs.append({
            "id": uid,
            "page_content": c,
            "metadata": {"source": source, "title": title, "chunk_id": i}
        })
    return docs
