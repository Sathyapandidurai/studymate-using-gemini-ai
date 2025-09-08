import streamlit as st
import fitz  # PyMuPDF for PDF text extraction
import os
from google import genai

# Initialize Gemini client (reads API key from env var)
client = genai.Client()

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "\n".join(page.get_text("text") for page in doc)
    return text

st.set_page_config(page_title="PDF Q&A ", page_icon="📄🤖")
st.title("PDF Q&A Bot ")
st.write("Upload a PDF and ask questions about its contents!")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
if uploaded_file:
    with st.spinner("Extracting text…"):
        pdf_text = extract_text_from_pdf(uploaded_file)

    preview = pdf_text[:1000] + ("..." if len(pdf_text) > 1000 else "")
    st.text_area("PDF Text Preview:", preview, height=200)

    question = st.text_input("Enter your question:")

    if question:
        with st.spinner("Generating answer…"):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"Context:\n{pdf_text}\n\nQuestion: {question}",
            )
            answer = response.text

        st.markdown("**Answer:**")
        st.write(answer)
