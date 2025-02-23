import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
import os

st.set_page_config(page_title="SmartPDF - PDF to Excel", layout="centered")

st.title("📄 SmartPDF - Convert PDF to Excel")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.write("Extracting text from PDF...")
    
    # Extrair texto
    def extract_text_from_pdf(pdf_path):
        doc = fitz.open(pdf_path)
        text = "\n".join([page.get_text("text") for page in doc])
        return text

    text = extract_text_from_pdf("temp.pdf")
    
    st.write("Generating structured data...")

    # Simulação da conversão em DataFrame
    data = {"Column1": ["Value1", "Value2"], "Column2": ["Value3", "Value4"]}
    df = pd.DataFrame(data)

    # Exibir DataFrame
    st.dataframe(df)

    # Salvar em Excel
    output_path = "converted.xlsx"
    df.to_excel(output_path, index=False)

    st.download_button("📥 Download Excel", open(output_path, "rb"), file_name="converted.xlsx")
