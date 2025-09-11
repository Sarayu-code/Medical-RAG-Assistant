from fastapi import FastAPI
from app.schemas import AskRequest, AskResponse, Source
from app.guardrails import emergency_flag, DISCLAIMER, instruction_prompt
from app.rag import retriever_singleton, format_context, synthesize_answer
from app.stt_tts import dummy_tts

# Serve Swagger UI at root so you see "Try it out" immediately
app = FastAPI(
    title="Medical RAG Voice Assistant",
    version="0.1.0",
    docs_url="/",
    redoc_url=None
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    # Guardrails
    emerg = emergency_flag(req.query)
    safety = {"disclaimer": DISCLAIMER, "emergency": emerg}

    # Retrieve documents
    docs = retriever_singleton.retrieve(req.query, k=req.top_k)

    # Compose system prompt and context (for future LLM use)
    system = instruction_prompt()
    _context = format_context(docs)  # currently not used by the stub answer

    # Synthesize (stub now; swap for local LLM like Ollama later)
    answer = synthesize_answer(req.query, docs, system)

    # Package sources (first 4)
    sources = []
    for d in docs[:4]:
        m = d.metadata or {}
        sources.append(Source(
            title=m.get("title", "Source"),
            url=m.get("source", ""),
            chunk_id=m.get("chunk_id", -1)
        ))

    # Optional TTS (swap dummy_tts for real TTS when ready)
    audio_b64 = dummy_tts(answer) if req.voice else None

    return AskResponse(answer=answer, sources=sources, safety=safety, audio_b64=audio_b64)
