# app/condition_links.py
import re
from typing import List, Dict, Optional

# Comprehensive medical conditions database
DISEASES = {
    # Common diseases
    "flu": {
        "keywords": ["flu", "influenza", "seasonal flu"],
        "condition": "Influenza (Flu)",
        "overview": "A viral infection that attacks the respiratory system.",
        "symptoms": "Fever, muscle aches, chills, fatigue, cough, headache, runny nose, sore throat",
        "causes": "Influenza viruses spread through droplets",
        "treatment": "Rest, fluids, antiviral medications, pain relievers",
        "prevention": "Annual flu vaccination, frequent handwashing",
        "links": [
            {"provider": "MedlinePlus", "title": "Flu - MedlinePlus", "url": "https://medlineplus.gov/flu.html"},
            {"provider": "CDC", "title": "Flu - CDC", "url": "https://www.cdc.gov/flu/"}
        ]
    },
    "covid19": {
        "keywords": ["covid", "covid-19", "coronavirus", "sars-cov-2"],
        "condition": "COVID-19",
        "overview": "A respiratory illness caused by the SARS-CoV-2 virus.",
        "symptoms": "Fever, cough, shortness of breath, fatigue, body aches, loss of taste or smell",
        "causes": "SARS-CoV-2 virus spread through respiratory droplets and airborne transmission",
        "treatment": "Rest, fluids, medications for symptoms, antiviral drugs in severe cases",
        "prevention": "Vaccination, mask wearing, social distancing, good hygiene",
        "links": [
            {"provider": "MedlinePlus", "title": "COVID-19 - MedlinePlus", "url": "https://medlineplus.gov/covid19coronavirusdisease2019.html"},
            {"provider": "CDC", "title": "COVID-19 - CDC", "url": "https://www.cdc.gov/coronavirus/2019-ncov/"}
        ]
    },
    "common_cold": {
        "keywords": ["common cold", "cold symptoms", "runny nose", "stuffy nose", "sniffles"],
        "condition": "Common Cold",
        "overview": "A viral infection of the upper respiratory tract.",
        "symptoms": "Runny nose, stuffy nose, sneezing, cough, sore throat, mild headache",
        "causes": "Viruses, especially rhinoviruses, spread through droplets",
        "treatment": "Rest, fluids, over-the-counter medications for symptoms",
        "prevention": "Frequent handwashing, avoid close contact with sick people",
        "links": [
            {"provider": "MedlinePlus", "title": "Common Cold - MedlinePlus", "url": "https://medlineplus.gov/commoncold.html"}
        ]
    },
    "diabetes": {
        "keywords": ["diabetes", "diabetic", "blood sugar", "insulin", "glucose"],
        "condition": "Diabetes",
        "overview": "A group of diseases that result in too much sugar in the blood.",
        "symptoms": "Increased thirst, frequent urination, hunger, fatigue, blurred vision",
        "causes": "Type 1: Immune system destroys insulin cells. Type 2: Insulin resistance",
        "treatment": "Insulin therapy, medications, blood sugar monitoring, diet, exercise",
        "prevention": "Maintain healthy weight, eat healthy foods, stay active",
        "links": [
            {"provider": "MedlinePlus", "title": "Diabetes - MedlinePlus", "url": "https://medlineplus.gov/diabetes.html"},
            {"provider": "CDC", "title": "Diabetes - CDC", "url": "https://www.cdc.gov/diabetes/"}
        ]
    },
    "hypertension": {
        "keywords": ["hypertension", "high blood pressure"],
        "condition": "High Blood Pressure",
        "overview": "A condition where blood force against artery walls is too high.",
        "symptoms": "Often no symptoms, headaches, shortness of breath, nosebleeds",
        "causes": "Age, family history, obesity, lack of activity, too much salt",
        "treatment": "Lifestyle changes, medications, regular monitoring",
        "prevention": "Healthy diet, regular exercise, maintain healthy weight",
        "links": [
            {"provider": "MedlinePlus", "title": "High Blood Pressure - MedlinePlus", "url": "https://medlineplus.gov/highbloodpressure.html"},
            {"provider": "CDC", "title": "High Blood Pressure - CDC", "url": "https://www.cdc.gov/bloodpressure/"}
        ]
    },
    "hypotension": {
        "keywords": ["low blood pressure", "hypotension"],
        "condition": "Low Blood Pressure",
        "overview": "A condition where blood pressure is lower than normal.",
        "symptoms": "Dizziness, fainting, fatigue, nausea, blurred vision",
        "causes": "Dehydration, heart problems, medications, severe infection",
        "treatment": "Increase fluid intake, medications, treat underlying causes",
        "prevention": "Stay hydrated, avoid sudden position changes, eat small frequent meals",
        "links": [
            {"provider": "MedlinePlus", "title": "Low Blood Pressure - MedlinePlus", "url": "https://medlineplus.gov/lowbloodpressure.html"}
        ]
    },
    "heart_disease": {
        "keywords": ["heart disease", "cardiac", "coronary", "heart attack", "chest pain", "heart pain", "heart ache", "angina"],
        "condition": "Heart Disease",
        "overview": "A range of conditions that affect the heart.",
        "symptoms": "Chest pain, shortness of breath, fatigue, irregular heartbeat",
        "causes": "High blood pressure, high cholesterol, smoking, diabetes, obesity",
        "treatment": "Medications, lifestyle changes, procedures",
        "prevention": "Healthy diet, regular exercise, don't smoke",
        "links": [
            {"provider": "MedlinePlus", "title": "Heart Disease - MedlinePlus", "url": "https://medlineplus.gov/heartdiseases.html"},
            {"provider": "CDC", "title": "Heart Disease - CDC", "url": "https://www.cdc.gov/heartdisease/"}
        ]
    },
    
    # Brain conditions
    "stroke": {
        "keywords": ["stroke", "brain attack", "cerebrovascular accident"],
        "condition": "Stroke",
        "overview": "Occurs when blood supply to brain is interrupted or reduced.",
        "symptoms": "Sudden numbness, confusion, trouble speaking, severe headache",
        "causes": "Blood clots, bleeding in brain, high blood pressure",
        "treatment": "Emergency care, clot-busting drugs, surgery, rehabilitation",
        "prevention": "Control blood pressure, don't smoke, exercise regularly",
        "links": [
            {"provider": "MedlinePlus", "title": "Stroke - MedlinePlus", "url": "https://medlineplus.gov/stroke.html"},
            {"provider": "CDC", "title": "Stroke - CDC", "url": "https://www.cdc.gov/stroke/"}
        ]
    },
    "brain_tumor": {
        "keywords": ["brain tumor", "brain cancer", "brain mass"],
        "condition": "Brain Tumor",
        "overview": "Abnormal growth of cells in the brain.",
        "symptoms": "Headaches, seizures, vision problems, memory issues, personality changes",
        "causes": "Unknown in most cases, genetic factors, radiation exposure",
        "treatment": "Surgery, radiation therapy, chemotherapy, targeted therapy",
        "prevention": "Avoid radiation exposure, healthy lifestyle",
        "links": [
            {"provider": "MedlinePlus", "title": "Brain Tumors - MedlinePlus", "url": "https://medlineplus.gov/braintumors.html"}
        ]
    },
    "migraine": {
        "keywords": ["migraine", "severe headache", "headache"],
        "condition": "Migraine",
        "overview": "A neurological condition causing severe throbbing pain.",
        "symptoms": "Severe headache, nausea, vomiting, sensitivity to light",
        "causes": "Genetics, hormonal changes, stress, certain foods",
        "treatment": "Pain medications, preventive medications, lifestyle changes",
        "prevention": "Identify triggers, regular sleep, stress management",
        "links": [
            {"provider": "MedlinePlus", "title": "Migraine - MedlinePlus", "url": "https://medlineplus.gov/migraine.html"}
        ]
    },
    
    # Muscle and pain conditions
    "muscle_ache": {
        "keywords": ["muscle ache", "muscle pain", "myalgia", "sore muscles"],
        "condition": "Muscle Aches",
        "overview": "Pain or discomfort in muscles throughout the body.",
        "symptoms": "Muscle pain, stiffness, tenderness, weakness",
        "causes": "Exercise, stress, infections, medications, autoimmune conditions",
        "treatment": "Rest, ice/heat, pain relievers, gentle stretching, massage",
        "prevention": "Proper warm-up, gradual exercise increase, stay hydrated",
        "links": [
            {"provider": "MedlinePlus", "title": "Muscle Cramps - MedlinePlus", "url": "https://medlineplus.gov/musclecramps.html"}
        ]
    },
    
    # Hormonal conditions
    "hormonal_imbalance": {
        "keywords": ["hormonal imbalance", "hormone imbalance", "endocrine disorder"],
        "condition": "Hormonal Imbalance",
        "overview": "When there's too much or too little of a hormone in the bloodstream.",
        "symptoms": "Irregular periods, weight changes, mood swings, fatigue, hair loss",
        "causes": "Age, stress, medications, medical conditions, lifestyle factors",
        "treatment": "Hormone therapy, lifestyle changes, medications, dietary changes",
        "prevention": "Healthy diet, regular exercise, stress management, adequate sleep",
        "links": [
            {"provider": "MedlinePlus", "title": "Hormones - MedlinePlus", "url": "https://medlineplus.gov/hormones.html"}
        ]
    },
    
    # Nose conditions
    "nosebleed": {
        "keywords": ["nosebleed", "nose bleed", "epistaxis", "bloody nose"],
        "condition": "Nosebleed",
        "overview": "Bleeding from the nose, usually from blood vessels in the nasal septum.",
        "symptoms": "Blood flowing from one or both nostrils",
        "causes": "Dry air, nose picking, allergies, medications, high blood pressure",
        "treatment": "Pinch nose, lean forward, apply ice, nasal sprays",
        "prevention": "Use humidifier, avoid nose picking, treat allergies",
        "links": [
            {"provider": "MedlinePlus", "title": "Nosebleeds - MedlinePlus", "url": "https://medlineplus.gov/nosebleeds.html"}
        ]
    },
    
    # Different types of cancer
    "breast_cancer": {
        "keywords": ["breast cancer", "breast tumor", "breast lump"],
        "condition": "Breast Cancer",
        "overview": "Cancer that forms in tissues of the breast.",
        "symptoms": "Breast lump, breast pain, nipple discharge, changes in breast size",
        "causes": "Age, genetics, family history, hormones, lifestyle factors",
        "treatment": "Surgery, chemotherapy, radiation therapy, hormone therapy",
        "prevention": "Regular screening, healthy lifestyle, limit alcohol",
        "links": [
            {"provider": "MedlinePlus", "title": "Breast Cancer - MedlinePlus", "url": "https://medlineplus.gov/breastcancer.html"},
            {"provider": "CDC", "title": "Breast Cancer - CDC", "url": "https://www.cdc.gov/cancer/breast/"}
        ]
    },
    "lung_cancer": {
        "keywords": ["lung cancer", "lung tumor", "lung carcinoma"],
        "condition": "Lung Cancer",
        "overview": "Cancer that begins in the lungs.",
        "symptoms": "Persistent cough, chest pain, shortness of breath, coughing up blood",
        "causes": "Smoking, secondhand smoke, radon, asbestos, air pollution",
        "treatment": "Surgery, chemotherapy, radiation therapy, targeted therapy",
        "prevention": "Don't smoke, avoid secondhand smoke, test home for radon",
        "links": [
            {"provider": "MedlinePlus", "title": "Lung Cancer - MedlinePlus", "url": "https://medlineplus.gov/lungcancer.html"},
            {"provider": "CDC", "title": "Lung Cancer - CDC", "url": "https://www.cdc.gov/cancer/lung/"}
        ]
    },
    "colon_cancer": {
        "keywords": ["colon cancer", "colorectal cancer", "bowel cancer"],
        "condition": "Colon Cancer",
        "overview": "Cancer that begins in the large intestine (colon).",
        "symptoms": "Changes in bowel habits, blood in stool, abdominal pain, weight loss",
        "causes": "Age, family history, inflammatory bowel disease, diet, lifestyle",
        "treatment": "Surgery, chemotherapy, radiation therapy, targeted therapy",
        "prevention": "Regular screening, healthy diet, exercise, limit alcohol",
        "links": [
            {"provider": "MedlinePlus", "title": "Colorectal Cancer - MedlinePlus", "url": "https://medlineplus.gov/colorectalcancer.html"},
            {"provider": "CDC", "title": "Colorectal Cancer - CDC", "url": "https://www.cdc.gov/cancer/colorectal/"}
        ]
    },
    "prostate_cancer": {
        "keywords": ["prostate cancer", "prostate tumor"],
        "condition": "Prostate Cancer",
        "overview": "Cancer that occurs in the prostate gland in men.",
        "symptoms": "Difficulty urinating, blood in urine, pelvic discomfort",
        "causes": "Age, race, family history, obesity",
        "treatment": "Surgery, radiation therapy, hormone therapy, chemotherapy",
        "prevention": "Healthy diet, regular exercise, maintain healthy weight",
        "links": [
            {"provider": "MedlinePlus", "title": "Prostate Cancer - MedlinePlus", "url": "https://medlineplus.gov/prostatecancer.html"},
            {"provider": "CDC", "title": "Prostate Cancer - CDC", "url": "https://www.cdc.gov/cancer/prostate/"}
        ]
    },
    "skin_cancer": {
        "keywords": ["skin cancer", "melanoma", "basal cell carcinoma", "squamous cell carcinoma"],
        "condition": "Skin Cancer",
        "overview": "Cancer that begins in the skin.",
        "symptoms": "New growths, changes in existing moles, sores that don't heal",
        "causes": "UV radiation from sun or tanning beds, fair skin, family history",
        "treatment": "Surgery, radiation therapy, chemotherapy, immunotherapy",
        "prevention": "Use sunscreen, avoid tanning beds, wear protective clothing",
        "links": [
            {"provider": "MedlinePlus", "title": "Skin Cancer - MedlinePlus", "url": "https://medlineplus.gov/skincancer.html"},
            {"provider": "CDC", "title": "Skin Cancer - CDC", "url": "https://www.cdc.gov/cancer/skin/"}
        ]
    },
    "ovarian_cancer": {
        "keywords": ["ovarian cancer", "ovary cancer"],
        "condition": "Ovarian Cancer",
        "overview": "Cancer that begins in the ovaries.",
        "symptoms": "Abdominal bloating, pelvic pain, difficulty eating, urinary urgency",
        "causes": "Age, genetics, family history, reproductive history",
        "treatment": "Surgery, chemotherapy, targeted therapy",
        "prevention": "Birth control pills, pregnancy, breastfeeding may reduce risk",
        "links": [
            {"provider": "MedlinePlus", "title": "Ovarian Cancer - MedlinePlus", "url": "https://medlineplus.gov/ovariancancer.html"},
            {"provider": "CDC", "title": "Ovarian Cancer - CDC", "url": "https://www.cdc.gov/cancer/ovarian/"}
        ]
    },
    "cervical_cancer": {
        "keywords": ["cervical cancer", "cervix cancer"],
        "condition": "Cervical Cancer",
        "overview": "Cancer that occurs in the cells of the cervix.",
        "symptoms": "Vaginal bleeding, pelvic pain, pain during intercourse",
        "causes": "HPV infection, smoking, weakened immune system",
        "treatment": "Surgery, radiation therapy, chemotherapy",
        "prevention": "HPV vaccination, regular Pap tests, safe sex practices",
        "links": [
            {"provider": "MedlinePlus", "title": "Cervical Cancer - MedlinePlus", "url": "https://medlineplus.gov/cervicalcancer.html"},
            {"provider": "CDC", "title": "Cervical Cancer - CDC", "url": "https://www.cdc.gov/cancer/cervical/"}
        ]
    },
    "pancreatic_cancer": {
        "keywords": ["pancreatic cancer", "pancreas cancer"],
        "condition": "Pancreatic Cancer",
        "overview": "Cancer that begins in the pancreas.",
        "symptoms": "Abdominal pain, weight loss, jaundice, new-onset diabetes",
        "causes": "Smoking, obesity, diabetes, family history, age",
        "treatment": "Surgery, chemotherapy, radiation therapy, targeted therapy",
        "prevention": "Don't smoke, maintain healthy weight, limit alcohol",
        "links": [
            {"provider": "MedlinePlus", "title": "Pancreatic Cancer - MedlinePlus", "url": "https://medlineplus.gov/pancreaticcancer.html"},
            {"provider": "CDC", "title": "Pancreatic Cancer - CDC", "url": "https://www.cdc.gov/cancer/pancreatic/"}
        ]
    },
    "liver_cancer": {
        "keywords": ["liver cancer", "hepatocellular carcinoma"],
        "condition": "Liver Cancer",
        "overview": "Cancer that begins in the liver.",
        "symptoms": "Weight loss, upper abdominal pain, nausea, jaundice",
        "causes": "Hepatitis B/C, cirrhosis, alcohol abuse, obesity",
        "treatment": "Surgery, liver transplant, chemotherapy, targeted therapy",
        "prevention": "Hepatitis B vaccination, limit alcohol, maintain healthy weight",
        "links": [
            {"provider": "MedlinePlus", "title": "Liver Cancer - MedlinePlus", "url": "https://medlineplus.gov/livercancer.html"},
            {"provider": "CDC", "title": "Liver Cancer - CDC", "url": "https://www.cdc.gov/cancer/liver/"}
        ]
    }
}

def _find_matching_disease(query: str) -> Optional[str]:
    """Find disease that matches query keywords with exact matching"""
    query_lower = query.lower()
    
    # Sort diseases by keyword length (longest first) to avoid partial matches
    diseases_sorted = sorted(DISEASES.items(), key=lambda x: max(len(kw) for kw in x[1]["keywords"]), reverse=True)
    
    for disease_key, disease_data in diseases_sorted:
        for keyword in disease_data["keywords"]:
            # Use word boundaries for exact matching
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, query_lower):
                return disease_key
    
    return None

def find_condition_pages(query: str) -> List[Dict[str, str]]:
    """Find condition pages with correct direct links"""
    disease_key = _find_matching_disease(query)
    
    if disease_key and disease_key in DISEASES:
        return DISEASES[disease_key]["links"]
    
    return []

def get_disease_summary(query: str) -> Optional[Dict[str, str]]:
    """Get disease summary from comprehensive database"""
    disease_key = _find_matching_disease(query)
    
    if disease_key and disease_key in DISEASES:
        disease_data = DISEASES[disease_key]
        return {
            "condition": disease_data["condition"],
            "overview": disease_data["overview"],
            "symptoms": disease_data["symptoms"],
            "causes": disease_data["causes"],
            "treatment": disease_data["treatment"],
            "prevention": disease_data["prevention"]
        }
    
    return None

def extract_symptoms_from_pages(pages: List[Dict[str, str]]) -> List[str]:
    """Return empty list - not implemented"""
    return []