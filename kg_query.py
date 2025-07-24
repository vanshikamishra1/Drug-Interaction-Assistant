import requests

def get_interaction_openfda(drug1, drug2):
    url = f"https://api.fda.gov/drug/label.json?search=drug_interactions:{drug1}+AND+drug_interactions:{drug2}&limit=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "results" in data and data["results"]:
            interactions = data["results"][0].get("drug_interactions", ["No details found."])
            interaction_text = interactions[0]
            # Basic keyword extraction for demo purposes
            severity = "High" if "severe" in interaction_text.lower() else "Unknown"
            risk = "Bleeding" if "bleed" in interaction_text.lower() else "Unknown"
            recommendation = "Avoid or monitor closely" if ("avoid" in interaction_text.lower() or "monitor" in interaction_text.lower()) else "Unknown"
            return {
                "severity": severity,
                "risk": risk,
                "recommendation": recommendation,
                "raw": interaction_text
            }
        else:
            return None
    else:
        return None