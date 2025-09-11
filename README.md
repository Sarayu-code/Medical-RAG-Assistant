# Medical RAG Voice Assistant

> A voice-enabled assistant that provides **grounded, cited** health information from authoritative sources (MedlinePlus, CDC). Not medical advice.

## Demo
- Backend: FastAPI (`/docs` for Swagger)
- Ask endpoint: `POST /ask { "query": "What are flu symptoms?", "voice": true }`
- The chatbot replies audibly, so users can hear the response.

## Architecture
- Ingestion → chunking → Chroma (MiniLM embeddings)
- Retrieval (k=6) → (optional re-ranking)
- LLM synthesis with strict safety prompt → citations
- Guardrails: emergency keyword flag + disclaimer
- (Week 3) STT/TTS for full voice UX

## Quickstart
```bash
make setup
make ingest
make run
# open http://localhost:8000/docs


#add a point - If symptoms are severe or worsening, consult a professional; call emergency services when appropriate (e.g., 911 in the U.S.). 