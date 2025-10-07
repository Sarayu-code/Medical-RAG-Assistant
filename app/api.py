from fastapi import FastAPI
from app.schemas import AskRequest, Source
from app.guardrails import emergency_flag, DISCLAIMER, instruction_prompt
from app.rag import retriever_singleton, format_context, synthesize_answer
from app.stt_tts import dummy_tts
from app.condition_links import find_condition_pages, extract_symptoms_from_pages, get_disease_summary

app = FastAPI(title="Medical RAG Voice Assistant", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(req: AskRequest):
    emerg = emergency_flag(req.query)
    safety = {"disclaimer": DISCLAIMER, "emergency": emerg}

    docs = retriever_singleton.retrieve(req.query, k=req.top_k)
    system = instruction_prompt()
    _ = format_context(docs)
    answer = synthesize_answer(req.query, docs, system)

    # Build sources from retrieved docs
    sources = []
    for d in docs[:4]:
        m = d.metadata or {}
        sources.append({
            "title": m.get("title", "Source"), 
            "url": m.get("source", ""), 
            "chunk_id": m.get("chunk_id", -1)
        })

    # NEW: condition pages (MedlinePlus + CDC)
    condition_pages = find_condition_pages(req.query)
    
    # NEW: disease summary from MedlinePlus
    disease_summary = get_disease_summary(req.query)

    if condition_pages:
        symptoms = extract_symptoms_from_pages(condition_pages)
        if symptoms:
            bullets = "\n".join(f"- {s}" for s in symptoms[:6])
            answer = f"**Symptoms (from reputable sources):**\n{bullets}\n\n{answer}"

    audio_b64 = dummy_tts(answer) if req.voice else None
    
    return {
        "answer": answer,
        "sources": sources,
        "safety": safety,
        "audio_b64": audio_b64,
        "condition_pages": condition_pages,
        "disease_summary": disease_summary
    }

@app.get("/")
def root():
    return {
        "message": "Medical RAG Assistant. POST to /ask with {'query': '...'}",
        "disclaimer": DISCLAIMER,
    }

# uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload
# streamlit run streamlit_app.py
