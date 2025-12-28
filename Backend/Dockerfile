FROM python:3.9.6-slim

# Define diretório de trabalho no container
WORKDIR /app

# Instala dependências de sistema básicas (se precisar compilar libs)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements primeiro (melhora cache)
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código do backend
COPY . .

# Expõe a porta da API
EXPOSE 8000

# Comando para subir o FastAPI com Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]