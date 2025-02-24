import fitz  # PyMuPDF
import pandas as pd
import os

def extract_text_from_pdf(pdf_path):
    """Extrai texto de um PDF e retorna como string"""
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text("text") for page in doc])
    return text

def convert_text_to_dataframe(text):
    """Converte o texto extraído em um DataFrame estruturado"""
    lines = text.split("\n")
    
    # Exemplo: Suponha que os dados tenham colunas separadas por espaços/tabs
    structured_data = [line.split() for line in lines if line.strip()]
    
    # Criar DataFrame (personalizar conforme estrutura do PDF)
    df = pd.DataFrame(structured_data)
    
    return df

def convert_pdf_to_excel(pdf_path, output_excel):
    """Converte um PDF para Excel"""
    text = extract_text_from_pdf(pdf_path)
    df = convert_text_to_dataframe(text)

    if df.empty:
        raise ValueError("Erro: O DataFrame gerado está vazio. O formato do PDF pode não ser suportado.")

    df.to_excel(output_excel, index=False)
    return output_excel
