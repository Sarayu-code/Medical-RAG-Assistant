import os
import base64
import requests
import streamlit as st

st.set_page_config(page_title="Medical RAG Assistant", page_icon="🩺", layout="centered")

# --------- Config (no visible backend URL control) ---------
API_BASE = os.environ.get("API_BASE", "http://localhost:8000")

st.sidebar.title("Settings")
top_k = st.sidebar.slider("Top-K (retrieval)", min_value=1, max_value=12, value=6)
voice = st.sidebar.checkbox("Speak the answer (voice)", value=False)
st.sidebar.markdown("---")
st.sidebar.caption("This app provides general health information, not medical advice.")

st.title("🩺 Medical RAG Assistant")
st.write("Ask a health-related question and get a concise answer with citations. **Not medical advice.**")

# ------------ Main form ------------
with st.form(key="ask_form", clear_on_submit=False):
    query = st.text_area(
        "Your question",
        placeholder="e.g., What are warning signs that chest pain is an emergency?",
        height=100,
    )
    submitted = st.form_submit_button("Ask")

if submitted:
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            try:
                payload = {"query": query.strip(), "top_k": top_k, "voice": voice}
                resp = requests.post(f"{API_BASE}/ask", json=payload, timeout=60)
            except Exception as e:
                st.error(f"Request failed: {e}")
                st.stop()

        if not resp.ok:
            st.error(f"Server error {resp.status_code}: {resp.text}")
            st.stop()

        try:
            data = resp.json()
        except Exception:
            st.error("Could not parse JSON response from server.")
            st.stop()

        # ------------ Safety / Emergency ------------
        safety = data.get("safety") or {}
        if safety.get("emergency"):
            st.error("⚠️ Potential emergency detected. If this is an emergency, call your local emergency number (e.g., 911 in the U.S.) now.")

        # ------------ Answer Card ------------
        with st.container(border=True):
            st.subheader("Answer")
            st.write(data.get("answer") or "_No answer returned._")

            # Audio playback (if present)
            if voice:
                audio_b64 = data.get("audio_b64")
                if audio_b64:
                    try:
                        audio_bytes = base64.b64decode(audio_b64)
                        st.audio(audio_bytes, format="audio/wav")
                    except Exception:
                        st.info("Audio returned but could not be decoded.")
                else:
                    st.caption("No audio returned. (Enable TTS in the backend or try again.)")

        # ------------ Sources ------------
        with st.container(border=True):
            st.subheader("Sources")
            sources = data.get("sources") or []
            if sources:
                seen = set()
                for s in sources:
                    title = s.get("title") or "Source"
                    url = s.get("url") or ""
                    key = url or title
                    if key in seen:
                        continue
                    seen.add(key)
                    if url:
                        st.markdown(f"• [{title}]({url})", unsafe_allow_html=True)
                    else:
                        st.markdown(f"• {title}", unsafe_allow_html=True)
            else:
                st.caption("No sources returned.")

        # ------------ Safety / Disclaimer ------------
        with st.container(border=True):
            st.subheader("Safety")
            disclaimer = safety.get("disclaimer") or "This assistant provides general health information, not medical advice."
            st.caption(disclaimer)