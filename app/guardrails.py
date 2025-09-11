EMERGENCY_KEYWORDS = [
    "severe chest pain","trouble breathing","blue lips","unconscious",
    "stroke","heart attack","suicidal","poisoning","overdose","heavy bleeding"
]

DISCLAIMER = (
  "This assistant provides general health information, not medical advice. "
  "If this is an emergency or you are in immediate danger, call your local emergency number (e.g., 911 in the U.S.) now."
)

def emergency_flag(text: str) -> bool:
    t = text.lower()
    return any(k in t for k in EMERGENCY_KEYWORDS)

def instruction_prompt():
    return (
      "You are a careful healthcare information assistant for laypeople.\n"
      "Rules:\n"
      "1) Answer concisely in plain language and ALWAYS cite sources with markdown links.\n"
      "2) Do NOT diagnose or prescribe. Encourage consulting a clinician when appropriate.\n"
      "3) Prefer authoritative sources (MedlinePlus, CDC) from provided context.\n"
      "4) If insufficient context, say so and suggest clearer query.\n"
    )
