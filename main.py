from pathlib import Path
import json
import pandas as pd
import fitz
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient


load_dotenv()

HF_TOKEN = os.getenv("HUG_TOKEN")  
MODEL_NAME = os.getenv("MODEL_ID")   # Ex: "meta-llama/Llama-3.2-1B-Instruct"

# EXTRACTION

def extract_metadata(pdf_path: str):
    f = Path(pdf_path)
    size = f.stat().st_size
    reader = fitz.open(str(f))
    return {
        "file_name": f.name,
        "file_size_bytes": size,
        "num_pages": reader.page_count,
    }


def extract_text_from_pdf(path):
    doc = fitz.open(path)
    return "\n".join(page.get_text() for page in doc)



# TRANSFORMATION

client = InferenceClient(
    token=HF_TOKEN
)

def transform_pdf_to_json(text: str):
    prompt = f"""
    Você é um modelo especializado em análise semântica. 
    Resuma o texto abaixo e retorne APENAS um JSON válido, sem comentários ou explicações.

    Regras:
    - Nunca repita elementos da lista.
    - Não use quebras de linha dentro dos valores.
    - O JSON DEVE ser perfeitamente válido.

    Estrutura obrigatória:

    {{
    "palavras_chave": ["kw1", "kw2", "kw3"],
    "tema": "uma frase curta e direta",
    "publico_alvo": "tipo de pessoa / setor"
    }}

    Texto para análise:

    {text[:3000]}
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.2,
    )

    
    cleaned = response.choices[0].message.content.strip()

    # Pegar somente o json
    if cleaned.startswith("{"):
        json_text = cleaned
    else:
        json_text = cleaned[cleaned.find("{"): cleaned.rfind("}") + 1]

    try:
        return json.loads(json_text)
    except Exception:
        
        return eval(json_text)


# ------------------------
# PIPELINE COMPLETO
# ------------------------

def generate_table(pdf_path: str):
    metadata = extract_metadata(pdf_path)
    text = extract_text_from_pdf(pdf_path)
    json_summary = transform_pdf_to_json(text)

    result = {**metadata, **json_summary}

    df = pd.DataFrame([result])
    
    return df


# RUN

if __name__ == "__main__":
    
    print("🔑 Token carregado?", "SIM" if HF_TOKEN else "NÃO ⚠")
    print("📌 Modelo:", MODEL_NAME)
    
    pdf_path = "turismo_e_etnicidade.pdf"
    output_file = Path(pdf_path).with_suffix(".table_inference.html")
    
    # LOAD
    
    df = generate_table(pdf_path)
    df.to_html('output.html', index=False) 
    
