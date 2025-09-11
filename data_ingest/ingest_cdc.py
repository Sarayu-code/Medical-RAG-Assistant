import httpx, json, os
from common import clean_html, chunk_text
from pathlib import Path

PAGES = [
  "https://www.cdc.gov/flu/symptoms/index.html",
  "https://www.cdc.gov/heartdisease/about.htm",
  "https://www.cdc.gov/dehydration/index.html"
]

OUT = Path(os.getenv("STORE_DIR", "./store"))
OUT.mkdir(parents=True, exist_ok=True)

def main():
    docs = []
    for url in PAGES:
        html = httpx.get(url, timeout=30).text
        title = url.split("/")[-2].replace("-", " ").title()
        text = clean_html(html)
        docs.extend(chunk_text(text, source=url, title=title))
    with open(OUT / "cdc.jsonl", "w", encoding="utf-8") as f:
        for d in docs:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    print(f"Ingested CDC to {OUT / 'cdc.jsonl'} ({len(docs)} chunks)")

if __name__ == "__main__":
    main()
