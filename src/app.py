import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
import os

# Garantir que a pasta "assets/" existe
ASSETS_DIR = "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

# Configuração do Streamlit
st.set_page_config(page_title="SmartPDF - PDF to Excel", layout="centered")

st.title("📄 SmartPDF - Convert PDF to Excel")

# Upload do arquivo PDF
uploaded_file = st.file_uploader("Upload um arquivo PDF", type=["pdf"])

# Função para extrair texto do PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text("text") for page in doc])
    return text

# Função para salvar DataFrame como Excel
def save_to_excel(df, output_path):
    df.to_excel(output_path, index=False)

# Processo de conversão do PDF para Excel
if uploaded_file:
    with st.spinner("Processando o PDF... ⏳"):
        # Criar o caminho do arquivo dentro de "assets/"
        temp_pdf_path = os.path.join(ASSETS_DIR, uploaded_file.name)

        # Salvar o arquivo na pasta correta
        with open(temp_pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Extrair texto
        extracted_text = extract_text_from_pdf(temp_pdf_path)

        # Criar um DataFrame simulando uma tabela estruturada
        data = {"Linha": extracted_text.split("\n")}
        df = pd.DataFrame(data)

        # Criar o caminho do arquivo Excel
        output_xlsx_path = os.path.join(ASSETS_DIR, "converted.xlsx")

        # Salvar DataFrame no Excel
        save_to_excel(df, output_xlsx_path)

        st.success("✅ Conversão concluída!")

        # Exibir DataFrame
        st.write("📊 Dados extraídos:")
        st.dataframe(df)

        # Botão de Download do Excel
        st.download_button(
            label="📥 Baixar Excel",
            data=open(output_xlsx_path, "rb"),
            file_name="converted.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
