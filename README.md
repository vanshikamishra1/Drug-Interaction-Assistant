# Medical Drug Interaction Assistant

A modern AI-powered assistant that checks for potential interactions between any two drugs using the openFDA API and provides clear, user-friendly medical advice with the help of a local large language model (Gemma 2B via Ollama).

---

## Features

- **User-Friendly UI:** Built with Streamlit for easy drug selection and question input.
- **Drug Name Extraction:** Uses spaCy and a curated drug list to extract drug names from user queries.
- **openFDA Powered:** Queries the openFDA API for drug interaction information.
- **LLM Explanations:** Uses Gemma 2B (via Ollama) to generate natural, user-friendly medical advice based on openFDA results.
- **Professional Output:** Displays results in a clean, readable format with AI advice, interaction details, and optional full data context.
- **History & PDF Export:** View past queries and download results as PDF.
- **Medical Disclaimer:** Reminds users to consult healthcare professionals for final decisions.

---

## Setup Instructions

1. **Clone the Repository**
    ```bash
    git clone <your-repo-url>
    cd medical-assistant
    ```

2. **Install Python Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Ollama and Gemma 2B**
    - [Install Ollama](https://ollama.com/)
    - Download the Gemma 2B model:
      ```bash
      ollama pull gemma:2b
      ```
    - Start the Ollama server:
      ```bash
      ollama serve
      ```

4. **Prepare Drug List**
    - Place your curated drug list in `utils/drug_names.txt` (one drug per line, matching openFDA supported drugs).

---

## Running the App

```bash
streamlit run app.py
```

---

## Usage

1. Select or type two drug names, or enter a natural language question.
2. Click **Check Interaction**.
3. View the interaction summary and AI medical advice.
4. Download the result as PDF if needed.

---
