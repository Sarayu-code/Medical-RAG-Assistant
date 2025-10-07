# data_ingest/search_and_ingest.py
import os, time, json, re
from pathlib import Path
import httpx
from typing import Iterable, List, Dict, Tuple
from duckduckgo_search import DDGS

# reuse your existing helpers
from common import clean_html, chunk_text

STORE_DIR = Path(os.getenv("STORE_DIR", "./store"))
STORE_DIR.mkdir(parents=True, exist_ok=True)

DOMAINS = {
    "medlineplus": "medlineplus.gov",
    "cdc": "cdc.gov",
}

UA = {"User-Agent": "MedicalRAGBot/0.1 (github.com/Sarayu-code/Medical-RAG-Assistant)"}

def ddg_site_search(query: str, site: str, max_results: int = 8) -> List[Dict]:
    """DuckDuckGo site: search; returns list of dict results."""
    q = f"{query} site:{site}"
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(q, max_results=max_results):
            # r often has keys: title, href (or link), body
            results.append(r)
    return results

def normalize_url(url: str) -> str:
    # strip anchors, tracking params; keep only http(s) to allowed domains
    url = re.sub(r"#.*$", "", url)
    url = re.sub(r"[?&]utm_[^=&]+=[^&]+", "", url)
    return url

def filter_domain(url: str, domain: str) -> bool:
    return (url.startswith("http://") or url.startswith("https://")) and (domain in url)

def fetch_html(url: str) -> Tuple[str, str]:
    """Return (title, html) or raise."""
    with httpx.Client(headers=UA, timeout=30.0, follow_redirects=True) as client:
        r = client.get(url)
        r.raise_for_status()
        html = r.text
        # quick title parse
        m = re.search(r"<title>(.*?)</title>", html, flags=re.I | re.S)
        title = m.group(1).strip() if m else url
        return title, html

def ingest_from_keywords(keywords: Iterable[str], max_per_site: int = 8, sleep_s: float = 0.5) -> int:
    """
    For each keyword, search both sites, dedupe URLs, fetch and ingest.
    Returns number of chunks written across both jsonl files.
    """
    keywords = [k.strip() for k in keywords if k and k.strip()]
    all_urls_by_site = {k: set() for k in DOMAINS}

    # 1) Search
    for kw in keywords:
        for site_key, domain in DOMAINS.items():
            results = ddg_site_search(kw, domain, max_results=max_per_site)
            for r in results:
                url = normalize_url(r.get("href") or r.get("link") or "")
                if url and filter_domain(url, domain):
                    all_urls_by_site[site_key].add(url)

    # 2) Fetch + chunk per site
    total_chunks = 0
    for site_key, domain in DOMAINS.items():
        out_path = STORE_DIR / f"{site_key}.jsonl"  # medlineplus.jsonl / cdc.jsonl
        docs = []
        for i, url in enumerate(sorted(all_urls_by_site[site_key])):
            try:
                title, html = fetch_html(url)
                text = clean_html(html)
                chunks = chunk_text(text, source=url, title=title, chunk_size=800, chunk_overlap=120)
                docs.extend(chunks)
                time.sleep(sleep_s)  # be nice
            except Exception as e:
                print(f"[warn] failed {url}: {e}")
                continue

        if docs:
            with open(out_path, "w", encoding="utf-8") as f:
                for d in docs:
                    f.write(json.dumps(d, ensure_ascii=False) + "\n")
            print(f"[ok] wrote {len(docs)} chunks to {out_path}")
            total_chunks += len(docs)
        else:
            print(f"[info] no docs for {site_key}")

    return total_chunks

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--keywords", type=str, required=True, help="comma-separated keywords, e.g. 'flu, fever, dehydration'")
    ap.add_argument("--max", type=int, default=8, help="max results per site per keyword")
    args = ap.parse_args()

    kws = [k.strip() for k in args.keywords.split(",")]
    n = ingest_from_keywords(kws, max_per_site=args.max)
    print(f"Total chunks ingested: {n}")
