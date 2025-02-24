import streamlit as st
import os
from backend.process_pdf import convert_pdf_to_excel

st.title("📄 SmartPDF - Convert PDF to Excel")

uploaded_file = st.file_uploader("Faça upload de um PDF", type=["pdf"])

if uploaded_file:
    # Salvar temporariamente o PDF
    pdf_path = f"assets/{uploaded_file.name}"
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.write("📄 Arquivo carregado com sucesso! Processando...")

    # Converter PDF para Excel
    try:
        excel_path = pdf_path.replace(".pdf", ".xlsx")
        convert_pdf_to_excel(pdf_path, excel_path)
        
        # Exibir botão de download
        st.success("✅ Conversão concluída!")
        st.download_button("📥 Baixar Excel", open(excel_path, "rb"), file_name="converted.xlsx")

    except Exception as e:
        st.error(f"Erro na conversão: {e}")
