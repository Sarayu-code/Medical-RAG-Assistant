# app/condition_links.py
import re
from typing import List, Dict

def _extract_disease_terms(query: str) -> List[str]:
    """Extract potential disease/condition terms from query with exact matching"""
    # Disease keywords mapped to actual MedlinePlus URL paths
    disease_map = {
        # Common diseases - using actual MedlinePlus URLs
        "flu": ["flu", "influenza"],
        "diabetes": ["diabetes", "diabetic"],
        "hypertension": ["hypertension", "high blood pressure"],
        "asthma": ["asthma"],
        "pneumonia": ["pneumonia"],
        "bronchitis": ["bronchitis"],
        "covid": ["covid", "coronavirus"],
        "heartdisease": ["heart disease", "cardiac disease"],
        "stroke": ["stroke"],
        "cancer": ["cancer"],
        "arthritis": ["arthritis"],
        "depression": ["depression"],
        "anxiety": ["anxiety"],
        "migraine": ["migraine"],
        "allergies": ["allergies", "allergy"],
        "eczema": ["eczema"],
        "psoriasis": ["psoriasis"],
        "hepatitis": ["hepatitis"],
        "kidneydiseases": ["kidney disease"],
        "osteoporosis": ["osteoporosis"],
        
        # Infectious diseases
        "cholera": ["cholera"],
        "chickenpox": ["chickenpox", "chicken pox", "varicella"],
        "measles": ["measles"],
        "mumps": ["mumps"],
        "rubella": ["rubella", "german measles"],
        "tuberculosis": ["tuberculosis", "tb"],
        "malaria": ["malaria"],
        "dengue": ["dengue"],
        "zika": ["zika"],
        "ebola": ["ebola"],
        "smallpox": ["smallpox"],
        "polio": ["polio", "poliomyelitis"],
        "meningitis": ["meningitis"],
        "sepsis": ["sepsis"],
        
        # Injuries and trauma
        "sprainsandstrains": ["sprain", "sprained", "strain", "muscle strain", "pulled muscle"],
        "fractures": ["fracture", "broken bone", "break", "broken"],
        "bruises": ["bruise", "contusion", "bruising"],
        "burns": ["burn", "burns", "burning"],
        "woundsandinjuries": ["cut", "laceration", "cuts", "wound"],
        "headinjuries": ["concussion", "head injury"],
        "dislocations": ["dislocation", "dislocated"],
        "whiplash": ["whiplash"],
        "backinjuries": ["back injury"],
        "neckinjuries": ["neck injury"],
        
        # Common symptoms/conditions
        "nosebleeds": ["nosebleed", "nose bleed", "bloody nose"],
        "fever": ["fever", "high temperature"],
        "headache": ["headache", "head pain"],
        "sorethroat": ["sore throat", "throat pain"],
        "cough": ["cough", "coughing"],
        "commoncold": ["runny nose", "stuffy nose", "cold"],
        "nausea": ["nausea", "feeling sick"],
        "vomiting": ["vomiting", "throwing up"],
        "diarrhea": ["diarrhea", "loose stools"],
        "constipation": ["constipation"],
        "fatigue": ["fatigue", "tiredness", "exhaustion"],
        "dizziness": ["dizziness", "dizzy"],
        "chestpain": ["chest pain"],
        "breathingproblems": ["shortness of breath", "breathing problems"],
        "abdominalpain": ["abdominal pain", "stomach pain", "belly pain"],
        "backpain": ["back pain"],
        "jointdisorders": ["joint pain"],
        "musclecramps": ["muscle pain", "muscle aches"],
        "rashes": ["rash", "skin rash"],
        "itching": ["itching", "itchy skin"],
        "edema": ["swelling", "swollen"],
        "bleeding": ["bleeding", "blood"],
        "fainting": ["fainting", "faint", "passed out"],
        "seizures": ["seizure", "convulsion"],
        "sleepdisorders": ["insomnia", "sleep problems", "can't sleep"],
        "weightloss": ["weight loss", "losing weight"],
        "obesity": ["weight gain", "gaining weight", "overweight"],
        
        # Chronic conditions
        "anemia": ["anemia"],
        "leukemia": ["leukemia"],
        "lymphoma": ["lymphoma"],
        "melanoma": ["melanoma"],
        "alzheimersdisease": ["alzheimer's disease", "alzheimers disease", "alzheimer"],
        "parkinsonsdisease": ["parkinson's disease", "parkinsons disease", "parkinson"],
        "epilepsy": ["epilepsy", "seizure disorder"],
        "fibromyalgia": ["fibromyalgia"],
        "lupus": ["lupus"],
        "multiplesclerosis": ["multiple sclerosis"],
        "thyroiddiseases": ["thyroid disease", "hypothyroidism", "hyperthyroidism", "thyroid"],
        "gout": ["gout"],
        "osteoarthritis": ["osteoarthritis"],
        "rheumatoidarthritis": ["rheumatoid arthritis"],
        "cataracts": ["cataracts"],
        "glaucoma": ["glaucoma"],
        "maculardegeneration": ["macular degeneration"],
        "hearingloss": ["hearing loss", "deafness"],
        "tinnitus": ["tinnitus"],
        "vertigo": ["vertigo"],
        
        # Digestive issues
        "pepticulcer": ["ulcer", "peptic ulcer"],
        "irritablebowelsyndrome": ["ibs", "irritable bowel syndrome"],
        "crohnsdisease": ["crohn's disease", "crohns disease"],
        "ulcerativecolitis": ["colitis", "ulcerative colitis"],
        "gastritis": ["gastritis"],
        "appendicitis": ["appendicitis"],
        "gallstones": ["gallstones", "gallbladder"],
        "gerd": ["acid reflux", "heartburn", "gerd"],
        
        # Women's health
        "pregnancy": ["pregnancy", "pregnant"],
        "menstruation": ["menstruation", "period", "menstrual"],
        "menopause": ["menopause"],
        "premenstrualsyndrome": ["pms", "premenstrual syndrome"],
        "polycysticovarysyndrome": ["pcos", "pcod", "polycystic ovary syndrome"],
        "endometriosis": ["endometriosis"],
        "fibroids": ["fibroids", "uterine fibroids"],
        "breastcancer": ["breast cancer"],
        "cervicalcancer": ["cervical cancer"],
        "ovariancancer": ["ovarian cancer"],
        "vaginitis": ["vaginitis", "yeast infection"],
        
        # Men's health
        "prostatediseases": ["prostate", "enlarged prostate"],
        "erectiledysfunction": ["erectile dysfunction", "ed"],
        "prostatecancer": ["prostate cancer"],
        "testicularcancer": ["testicular cancer"],
        
        # Mental health
        "stress": ["stress", "stressed"],
        "panicdisorder": ["panic attack", "panic disorder"],
        "posttraumaticstressdisorder": ["ptsd", "post traumatic stress"],
        "bipolardisorder": ["bipolar", "manic depression"],
        "schizophrenia": ["schizophrenia"],
        "eatingdisorders": ["eating disorder", "anorexia", "bulimia"],
        "addictionandsubstanceabuse": ["addiction", "substance abuse", "drug abuse"],
        
        # Skin conditions
        "acne": ["acne", "pimples"],
        "dermatitis": ["dermatitis"],
        "hives": ["hives", "urticaria"],
        "warts": ["warts"],
        "fungalinfections": ["fungal infection", "athlete's foot", "ringworm"],
        "skininfections": ["skin infection"],
        "skincancer": ["skin cancer"],
        
        # Eye/ear conditions
        "conjunctivitis": ["pink eye", "conjunctivitis"],
        "stye": ["stye", "eye infection"],
        "earinfections": ["ear infection", "earache"],
        "hearingdisorders": ["swimmer's ear"],
        
        # Respiratory
        "sinusitis": ["sinusitis", "sinus infection"],
        "tonsillitis": ["tonsillitis"],
        "laryngitis": ["laryngitis"],
        "whoopingcough": ["whooping cough", "pertussis"],
        "copd": ["copd", "chronic obstructive pulmonary disease"],
        "lungcancer": ["lung cancer"],
        
        # Cardiovascular
        "heartattack": ["heart attack", "myocardial infarction"],
        "angina": ["angina"],
        "heartfailure": ["heart failure"],
        "arrhythmia": ["arrhythmia", "irregular heartbeat"],
        "atherosclerosis": ["atherosclerosis"],
        "bloodclots": ["blood clots", "thrombosis"],
        "varicoseveins": ["varicose veins"],
        
        # Endocrine
        "diabetestype1": ["type 1 diabetes"],
        "diabetestype2": ["type 2 diabetes"],
        "gestationaldiabetes": ["gestational diabetes"],
        "hypoglycemia": ["hypoglycemia", "low blood sugar"],
        "hyperglycemia": ["hyperglycemia", "high blood sugar"],
        "adrenaldisorders": ["adrenal disorders"],
        
        # Bone and joint
        "osteoporosis": ["osteoporosis"],
        "bonecancer": ["bone cancer"],
        "bonediseases": ["bone diseases"],
        "jointreplacementsurgery": ["joint replacement"],
        "scoliosis": ["scoliosis"],
        
        # Kidney and urinary
        "kidneystones": ["kidney stones"],
        "urinarytractinfections": ["uti", "urinary tract infection"],
        "kidneyfailure": ["kidney failure"],
        "bladderproblems": ["bladder problems"],
        "incontinence": ["incontinence"],
        
        # Blood disorders
        "hemophilia": ["hemophilia"],
        "sicklecelldisease": ["sickle cell disease"],
        "thalassemia": ["thalassemia"],
        "bloodtransfusion": ["blood transfusion"],
        
        # Other common conditions
        "dehydration": ["dehydration"],
        "foodpoisoning": ["food poisoning"],
        "motionsickness": ["motion sickness", "car sickness"],
        "jetlag": ["jet lag"],
        "sunburn": ["sunburn"],
        "heatillness": ["heat exhaustion", "heat stroke"],
        "frostbite": ["frostbite"],
        "hypothermia": ["hypothermia"],
        "poisoning": ["poisoning"],
        "allergicreactions": ["allergic reaction", "anaphylaxis"],
        
        # Nutritional
        "vitamins": ["vitamins", "vitamin deficiency"],
        "minerals": ["minerals", "mineral deficiency"],
        "malnutrition": ["malnutrition"],
        "dietaryfiber": ["fiber", "dietary fiber"],
        
        # Age-related
        "aging": ["aging", "elderly health"],
        "childhealth": ["child health", "pediatric"],
        "adolescenthealth": ["adolescent health", "teen health"],
        
        # Preventive care
        "immunization": ["vaccination", "immunization", "vaccines"],
        "healthscreening": ["health screening", "checkup"],
        "cancerscreening": ["cancer screening"],
        
        # Emergency conditions
        "emergencies": ["emergency", "medical emergency"],
        "firstaid": ["first aid"],
        "cpr": ["cpr", "cardiopulmonary resuscitation"],
        "choking": ["choking"],
        "shock": ["shock", "medical shock"]
    }
    
    query_lower = query.lower().strip()
    found_terms = []
    
    # First, try exact phrase matching for multi-word conditions
    for disease, variations in disease_map.items():
        for variation in variations:
            # Use word boundaries for exact matching
            pattern = r'\b' + re.escape(variation) + r'\b'
            if re.search(pattern, query_lower):
                found_terms.append(disease)
                break
    
    # Remove duplicates while preserving order
    seen = set()
    unique_terms = []
    for term in found_terms:
        if term not in seen:
            seen.add(term)
            unique_terms.append(term)
    
    return unique_terms[:1]  # Return only the first match for accuracy

def find_condition_pages(query: str) -> List[Dict[str, str]]:
    """Find direct condition pages on MedlinePlus and CDC"""
    disease_terms = _extract_disease_terms(query)
    
    condition_pages = []
    
    for term in disease_terms:
        # MedlinePlus direct links using actual URL structure
        medline_url = f"https://medlineplus.gov/{term}.html"
        condition_pages.append({
            "provider": "MedlinePlus",
            "title": f"{term.replace('', ' ').title()} - MedlinePlus",
            "url": medline_url
        })
        
        # CDC direct links - only for diseases that typically have CDC pages
        cdc_diseases = ["flu", "diabetes", "heartdisease", "stroke", "cancer", "asthma", "tuberculosis", 
                       "hepatitis", "cholera", "measles", "mumps", "rubella", "malaria", "dengue", 
                       "zika", "ebola", "smallpox", "polio", "meningitis", "sepsis", "covid"]
        
        if term in cdc_diseases:
            cdc_url = f"https://www.cdc.gov/{term}/index.html"
            condition_pages.append({
                "provider": "CDC", 
                "title": f"{term.replace('', ' ').title()} - CDC",
                "url": cdc_url
            })
    
    return condition_pages

def extract_symptoms_from_pages(pages: List[Dict[str, str]]) -> List[str]:
    """Placeholder for symptom extraction"""
    return []