import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
import os
import pytesseract
from pdf2image import convert_from_path

# Criar a pasta assets/ caso não exista
ASSETS_DIR = "assets"
if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)

# Configuração do Streamlit
st.set_page_config(page_title="SmartPDF - PDF to Excel", layout="centered")

st.title("📄 SmartPDF - Convert PDF to Excel")

# Upload do arquivo PDF
uploaded_file = st.file_uploader("Upload um arquivo PDF", type=["pdf"])

# Função para verificar se o PDF tem texto extraível
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = []
    for page in doc:
        extracted_text = page.get_text("text")
        if extracted_text.strip():
            text.append(extracted_text.strip())
    return "\n".join(text)

# Função para extrair texto de imagens (OCR)
def extract_text_from_images(pdf_path):
    images = convert_from_path(pdf_path)
    text = []
    for img in images:
        extracted_text = pytesseract.image_to_string(img, lang="por")
        text.append(extracted_text.strip())
    return "\n".join(text)

# Função para converter texto em DataFrame estruturado
def convert_text_to_dataframe(text):
    lines = text.split("\n")
    data = {"Linha": [], "Conteúdo": []}
    for idx, line in enumerate(lines):
        if line.strip():
            data["Linha"].append(idx + 1)
            data["Conteúdo"].append(line)
    return pd.DataFrame(data)

# Função para salvar DataFrame como Excel
def save_to_excel(df, output_path):
    df.to_excel(output_path, index=False)

# Processo de conversão do PDF para Excel
if uploaded_file:
    with st.spinner("Processando o PDF... ⏳"):
        temp_pdf_path = os.path.join(ASSETS_DIR, uploaded_file.name)

        # Salvar o arquivo corretamente
        with open(temp_pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Tentar extrair texto diretamente do PDF
        extracted_text = extract_text_from_pdf(temp_pdf_path)

        # Se não houver texto extraído, usar OCR
        if not extracted_text.strip():
            st.warning("🔍 O PDF pode ser um documento escaneado. Usando OCR...")
            extracted_text = extract_text_from_images(temp_pdf_path)

        # Criar DataFrame
        df = convert_text_to_dataframe(extracted_text)

        # Criar e salvar arquivo Excel
        output_xlsx_path = os.path.join(ASSETS_DIR, "converted.xlsx")
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
