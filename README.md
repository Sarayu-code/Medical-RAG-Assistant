# 🩺 Medical RAG Assistant

> A comprehensive medical assistant that provides **grounded, cited** health information from authoritative sources (MedlinePlus, CDC). **Not medical advice.**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-green.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 Features

### 🔍 Comprehensive Medical Coverage
- **35+ Medical Conditions** with detailed summaries
- **Multiple Cancer Types** (breast, lung, colon, prostate, skin, ovarian, cervical, pancreatic, liver)
- **Physical Injuries** (sprains, fractures, bruises)
- **Women's Health** (menopause, PCOS, hormonal imbalance)
- **Neurological Conditions** (stroke, brain tumors, migraines)
- **Infectious Diseases** (COVID-19, flu, tuberculosis, measles, cholera)
- **Chronic Conditions** (diabetes, hypertension, heart disease, asthma)

### 📋 Disease Information Includes
- **Overview**: Clear explanation of the condition
- **Symptoms**: Key signs to watch for
- **Causes**: What leads to the condition
- **Treatment**: Available treatment options
- **Prevention**: How to reduce risk
- **Direct Links**: MedlinePlus and CDC official pages

### 🛡️ Safety Features
- **Emergency Detection**: Flags potential emergency situations
- **Medical Disclaimers**: Clear warnings that this is not medical advice
- **Professional Guidance**: Encourages consulting healthcare providers
- **Emergency Contact Info**: Reminds users to call 911 when appropriate

### 🎯 Smart Matching
- **Intelligent Keyword Detection**: Matches similar terms (heart pain = chest pain)
- **Exact Word Boundaries**: Prevents false matches
- **Priority Matching**: Longer, more specific terms matched first

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/Medical-RAG-Assistant.git
cd Medical-RAG-Assistant
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Start the backend API**
```bash
uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload
```

4. **Start the frontend (new terminal)**
```bash
streamlit run streamlit_app.py
```

5. **Access the application**
- **Web Interface**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 💻 Usage Examples

### Web Interface
Ask questions like:
- "What are diabetes symptoms?"
- "How to treat a sprained ankle?"
- "COVID-19 prevention methods"
- "Breast cancer screening guidelines"
- "Low blood pressure causes"

### API Usage
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the symptoms of heart disease?",
    "top_k": 6,
    "voice": false
  }'
```

### Response Format
```json
{
  "answer": "General health guidance...",
  "condition_pages": [
    {
      "provider": "MedlinePlus",
      "title": "Heart Disease - MedlinePlus",
      "url": "https://medlineplus.gov/heartdiseases.html"
    }
  ],
  "disease_summary": {
    "condition": "Heart Disease",
    "overview": "A range of conditions that affect the heart.",
    "symptoms": "Chest pain, shortness of breath, fatigue...",
    "causes": "High blood pressure, high cholesterol...",
    "treatment": "Medications, lifestyle changes...",
    "prevention": "Healthy diet, regular exercise..."
  },
  "safety": {
    "disclaimer": "This is for informational purposes only...",
    "emergency": false
  }
}
```

## 🏗️ Architecture

### Backend (FastAPI)
- **API Endpoints**: `/ask`, `/health`, `/`
- **RAG System**: Retrieval-Augmented Generation with embeddings
- **Disease Database**: Comprehensive static medical knowledge base
- **Safety Guardrails**: Emergency detection and medical disclaimers

### Frontend (Streamlit)
- **Clean UI**: Intuitive medical query interface
- **Disease Summaries**: Structured medical information display
- **Direct Links**: Quick access to authoritative sources
- **Safety Warnings**: Prominent emergency and disclaimer notices

### Data Sources
- **MedlinePlus**: National Library of Medicine
- **CDC**: Centers for Disease Control and Prevention
- **Embeddings**: Sentence transformers for semantic search
- **Static Database**: 35+ curated medical conditions

## 📁 Project Structure

```
Medical-RAG-Assistant/
├── app/
│   ├── api.py              # FastAPI backend
│   ├── schemas.py          # Pydantic models
│   ├── rag.py             # RAG retrieval system
│   ├── condition_links.py  # Disease database
│   ├── guardrails.py      # Safety features
│   └── stt_tts.py         # Voice features (placeholder)
├── streamlit_app.py       # Frontend interface
├── requirements.txt       # Dependencies
├── store/                 # Data storage
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables
```bash
# Optional configurations
EMBEDDINGS_MODEL=all-MiniLM-L6-v2  # Sentence transformer model
STORE_DIR=./store                   # Data storage directory
API_BASE=http://localhost:8000      # Backend URL for frontend
```

### Customization
- **Add new diseases**: Update `DISEASES` dictionary in `condition_links.py`
- **Modify safety rules**: Edit `guardrails.py`
- **Change UI**: Customize `streamlit_app.py`
- **Update embeddings**: Modify `EMBEDDINGS_MODEL` in `rag.py`

## 🛡️ Safety & Disclaimers

### ⚠️ Important Notices
- **Not Medical Advice**: This tool provides general health information only
- **Emergency Situations**: Call 911 or local emergency services for emergencies
- **Professional Consultation**: Always consult healthcare providers for medical decisions
- **Information Purpose**: Content is for educational purposes only

### Emergency Detection
The system automatically flags queries containing emergency keywords:
- "emergency", "urgent", "911"
- "chest pain", "heart attack", "stroke"
- And displays prominent warnings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-condition`)
3. Add medical conditions to `condition_links.py`
4. Test thoroughly with various queries
5. Commit changes (`git commit -am 'Add new medical condition'`)
6. Push to branch (`git push origin feature/new-condition`)
7. Create Pull Request

### Adding New Medical Conditions
```python
"condition_name": {
    "keywords": ["keyword1", "keyword2", "synonym"],
    "condition": "Display Name",
    "overview": "Brief description...",
    "symptoms": "List of symptoms...",
    "causes": "What causes it...",
    "treatment": "Treatment options...",
    "prevention": "Prevention methods...",
    "links": [
        {"provider": "MedlinePlus", "title": "...", "url": "..."},
        {"provider": "CDC", "title": "...", "url": "..."}
    ]
}
```

## 📈 Performance

- **Response Time**: < 2 seconds for most queries
- **Accuracy**: Exact keyword matching prevents false positives
- **Coverage**: 35+ medical conditions with comprehensive information
- **Reliability**: Static database ensures consistent responses
- **Scalability**: Lightweight architecture supports high query volumes

## 🔮 Future Enhancements

- [ ] **Voice Integration**: Real speech-to-text and text-to-speech
- [ ] **LLM Integration**: Advanced language model for better responses
- [ ] **More Conditions**: Expand to 100+ medical conditions
- [ ] **Multilingual Support**: Support for multiple languages
- [ ] **Mobile App**: Native mobile applications
- [ ] **Symptom Checker**: Interactive symptom assessment tool
- [ ] **Drug Information**: Medication database integration
- [ ] **Doctor Finder**: Healthcare provider location service

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **MedlinePlus**: National Library of Medicine for authoritative health information
- **CDC**: Centers for Disease Control and Prevention for public health data
- **FastAPI**: Modern, fast web framework for building APIs
- **Streamlit**: Open-source app framework for machine learning projects
- **Sentence Transformers**: State-of-the-art text embeddings

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/Medical-RAG-Assistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/Medical-RAG-Assistant/discussions)
- **Email**: spoddutoori@umass.edu

---

**⚠️ Medical Disclaimer**: This application provides general health information and is not intended as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. Never disregard professional medical advice or delay in seeking it because of something you have read in this application. If you think you may have a medical emergency, call your doctor or 911 immediately.
