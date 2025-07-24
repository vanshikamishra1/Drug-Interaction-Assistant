import re
import os

def load_drug_list():
    # Load drug names from drug_names.txt
    path = os.path.join(os.path.dirname(__file__), "drug_names.txt")
    with open(path, "r", encoding="utf-8") as f:
        return set(line.strip().lower() for line in f if line.strip())


drug_set = load_drug_list()

def extract_drugs(text):
    
    tokens = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    found = [t for t in tokens if t in drug_set]
    return list(set(found))