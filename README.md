# 📄 ETL de Documentos PDF com IA (Hugging Face + Python)

Este projeto aplica um processo de **ETL (Extract, Transform, Load)** para automatizar a leitura de arquivos PDF, realizar análise semântica por meio de um modelo de IA hospedado no Hugging Face e gerar uma tabela estruturada como saída.

---

## 🚀 Tecnologias utilizadas

| Componente                 | Descrição                                |
| -------------------------- | ---------------------------------------- |
| Python 3.10+               | Linguagem principal                      |
| PyMuPDF (`fitz`)           | Extração de conteúdo PDF                 |
| Hugging Face Inference API | Inferência via LLM (modelo configurável) |
| Pandas                     | Criação da tabela de saída               |
| dotenv                     | Gerenciamento seguro de tokens           |

---

## 🧠 Visão Geral da Arquitetura ETL

O processo segue três etapas principais:

---

### **1️⃣ EXTRAÇÃO — Leitura do PDF**

Nesta etapa o script:

✔ Lê o arquivo PDF
✔ Extrai o texto integral
✔ Coleta metadados estruturados, como:

* Nome do arquivo
* Tamanho em bytes
* Número de páginas

Funções responsáveis:

```python
extract_metadata()
extract_text_from_pdf()
```

---

### **2️⃣ TRANSFORMAÇÃO — Análise Semântica com IA**

Aqui o conteúdo do PDF é enviado ao modelo configurado no Hugging Face via API.

O modelo deve retornar **exclusivamente um JSON válido** contendo:

```json
{
  "palavras_chave": ["kw1", "kw2", "kw3"],
  "tema": "uma frase curta e direta",
  "publico_alvo": "tipo de pessoa / setor"
}
```

Essa etapa:

* Reduz, interpreta e organiza o conteúdo
* Remove redundâncias
* Padroniza campos

Função responsável:

```python
transform_pdf_to_json()
```

---

### **3️⃣ CARREGAMENTO — Geração da Tabela Final**

Os dados extraídos e transformados são unidos em um único dicionário e convertidos para tabela utilizando Pandas.

A saída final pode ser exportada para:

* `.html` (implementado)
* `.xlsx`
* `.csv` (opcional)

Função responsável:

```python
generate_table()
```

---

## 📦 Variáveis de Ambiente `.env`

Antes de executar o script, configure:

```
HUG_TOKEN=seu_token_aqui
MODEL_ID=meta-llama/Llama-3.2-1B-Instruct
```

---

## ▶️ Como executar

1. Instale dependências:

```sh
pip install -r requirements.txt
```

2. Certifique-se de ter o token do Hugging Face configurado no `.env`.

3. Execute o script:

```sh
python main.py
```

4. A saída será salva como:

```
output.html
```

---

## 📝 Exemplo de saída esperada

| file_name     | file_size_bytes | num_pages | palavras_chave                       | tema                           | publico_alvo                                |
| ------------- | --------------- | --------- | ------------------------------------ | ------------------------------ | ------------------------------------------- |
| documento.pdf | 48322           | 6         | ["turismo", "cultura", "identidade"] | Turismo e diversidade cultural | Pesquisadores, estudantes e setor turístico |

---

## 🛠 Melhorias futuras

* [ ] Suporte para múltiplos PDFs simultâneos
* [ ] Exportação CSV e XLSX automatizada
* [ ] Dashboard analítico com Streamlit

---

## 📚 Licença

Este projeto é open-source sob licença **MIT**.

