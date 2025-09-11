from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class AskRequest(BaseModel):
    query: str
    top_k: int = 6
    use_reranker: bool = True
    voice: bool = False  # triggers TTS in /ask

class Source(BaseModel):
    title: str
    url: str
    chunk_id: int

class AskResponse(BaseModel):
    answer: str
    sources: List[Source]
    safety: Dict[str, Any] = Field(default_factory=dict)
    audio_b64: Optional[str] = None
