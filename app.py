import streamlit as st
from utils.drug_extractor import extract_drugs
from utils.kg_query import get_interaction_openfda
from utils.llm import query_llm
import base64
from fpdf import FPDF

def load_drug_list():
    with open("utils/drug_names.txt", "r", encoding="utf-8") as f:
        return sorted([line.strip().capitalize() for line in f if line.strip()])

drug_list = load_drug_list()

st.set_page_config(page_title="Medical Drug Interaction Assistant", layout="centered")

if "history" not in st.session_state:
    st.session_state["history"] = []

with st.sidebar:
    st.title("Powered by")
    st.markdown("- openFDA API")
    st.markdown("- spaCy (for NLP)")
    st.markdown("- Ollama + Gemma 2B")
    st.markdown("- Streamlit")
    st.markdown("---")
    st.subheader("Your Q&A History")
    for q, a in st.session_state["history"]:
        st.markdown(f"**Q:** {q}")
        st.markdown(f"**A:** {a}")
        st.markdown("---")
    if st.button("Clear History"):
        st.session_state["history"] = []

st.title("Medical Drug Interaction Assistant")

st.markdown("Enter your medical question (e.g., Can I take Ibuprofen with Warfarin?)")
drug1 = st.selectbox("First Drug", drug_list, key="drug1")
drug2 = st.selectbox("Second Drug", drug_list, key="drug2")
question = st.text_input("Type your full question here (optional):", "")

if st.button("Check Interaction"):
    if not question.strip():
        question = f"Can I take {drug1} with {drug2}?"
    drugs_found = extract_drugs(question) if question.strip() else [drug1.lower(), drug2.lower()]
    if len(drugs_found) < 2:
        drugs_found = [drug1.lower(), drug2.lower()]

    with st.spinner("Analyzing your question and checking medical knowledge graph..."):
        result = get_interaction_openfda(drugs_found[0], drugs_found[1])
        if result:
            st.subheader("User Query")
            st.info(question)
            st.markdown(f"**Drugs Identified:** {drug1}, {drug2}")

            st.subheader("Interaction Summary")
            st.markdown(f"""
            <div style="background-color:#f8f9fa;padding:15px;border-radius:8px;">
            <b>Severity:</b> {result['severity']}<br>
            <b>Risk:</b> {result['risk']}<br>
            <b>Recommendation:</b> {result['recommendation']}
            </div>
            """, unsafe_allow_html=True)

            context = (
                f"- Severity: {result['severity']}\n"
                f"- Risk: {result['risk']}\n"
                f"- Recommendation: {result['recommendation']}"
            )
        else:
            st.subheader("User Query")
            st.info(question)
            st.markdown(f"**Drugs Identified:** {drug1}, {drug2}")

            st.subheader("Interaction Summary")
            st.warning("No known interaction found in the openFDA database for this drug combination. This may mean the combination is considered safe or not listed in FDA data. Always consult a healthcare professional.")

            context = f"No interaction data found for {drug1} and {drug2} in the openFDA database."

        llm_prompt = (
            f"A patient asked: {question}\n"
            f"Based on this data:\n"
            f"{context}\n"
            "Please respond clearly and simply."
        )
        llm_response = query_llm(context, question)
        st.session_state["history"].append((question, llm_response))

        st.subheader("AI Medical Advice")
        st.success(llm_response)

        # Show full FDA text in expandable section
        if result and result.get("raw"):
            with st.expander("Show Full FDA Interaction Text"):
                st.write(result["raw"])

        # Download as PDF
        if st.button("Download Result as PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Medical Drug Interaction Assistant", ln=True, align="C")
            pdf.ln(10)
            pdf.cell(200, 10, txt=f"Question: {question}", ln=True)
            pdf.ln(5)
            pdf.multi_cell(0, 10, f"Drugs Identified: {drug1}, {drug2}")
            pdf.ln(5)
            if result:
                pdf.multi_cell(0, 10, f"Severity: {result['severity']}")
                pdf.multi_cell(0, 10, f"Risk: {result['risk']}")
                pdf.multi_cell(0, 10, f"Recommendation: {result['recommendation']}")
            else:
                pdf.multi_cell(0, 10, "No known interaction found in the openFDA database.")
            pdf.ln(5)
            pdf.multi_cell(0, 10, f"AI Medical Advice:\n{llm_response}")
            if result and result.get("raw"):
                pdf.ln(5)
                pdf.multi_cell(0, 10, f"Full FDA Interaction Text:\n{result['raw']}")
            pdf_output = "result.pdf"
            pdf.output(pdf_output)
            with open(pdf_output, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                href = f'<a href="data:application/octet-stream;base64,{b64}" download="result.pdf">Download PDF</a>'
                st.markdown(href, unsafe_allow_html=True)
