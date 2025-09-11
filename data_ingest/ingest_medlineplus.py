import httpx, json, os
from common import clean_html, chunk_text
from pathlib import Path

TOPICS = [
    "https://medlineplus.gov/flu.html",
    "https://medlineplus.gov/fever.html",
    "https://medlineplus.gov/chestpain.html",
    "https://medlineplus.gov/dehydration.html",
]

OUT = Path(os.getenv("STORE_DIR", "./store"))
OUT.mkdir(parents=True, exist_ok=True)

def fetch(url: str) -> str:
    r = httpx.get(url, timeout=30)
    r.raise_for_status()
    return r.text

def main():
    docs = []
    for url in TOPICS:
        html = fetch(url)
        text = clean_html(html)
        title = url.split("/")[-1].replace(".html","").replace("-", " ").title()
        docs.extend(chunk_text(text, source=url, title=title))
    with open(OUT / "medlineplus.jsonl", "w", encoding="utf-8") as f:
        for d in docs:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    print(f"Ingested MedlinePlus to {OUT / 'medlineplus.jsonl'} ({len(docs)} chunks)")

if __name__ == "__main__":
    main()
