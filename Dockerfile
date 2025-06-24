# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Cria diretório de trabalho
WORKDIR /app

# Copia arquivos do projeto
COPY model_treino.py base_com_hdr_e_gdp.xlsx ./

# Instala dependências Python
RUN pip install --upgrade pip
RUN pip install streamlit pandas numpy scikit-learn joblib scipy openpyxl

# Expõe a porta padrão do Streamlit
EXPOSE 8501

# Define variável de ambiente para Streamlit usar a porta do Railway
ENV PORT 8501

# Comando para rodar o app
CMD streamlit run model_treino.py --server.port $PORT --server.address 0.0.0.0
