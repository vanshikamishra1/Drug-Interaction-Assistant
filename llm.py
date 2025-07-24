import requests

def query_llm(context, question):
    prompt = (
        f"A patient asked: {question}\n"
        f"Based on this data:\n"
        f"{context}\n"
        "Please respond clearly and simply."
    )
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "gemma:2b", "prompt": prompt, "stream": False}
    )
    if response.status_code == 200:
        return response.json()["response"].strip()
    else:
        return "LLM error: Could not get a response."