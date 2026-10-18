FROM python:3.11-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Instala as dependências necessárias do sistema (opcional, mas bom para garantir builds limpos)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de requerimentos e instala as dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o restante do código do microsserviço para o contêiner
COPY . .

# Expõe a porta que o serviço vai escutar
EXPOSE 5002

# Comando para rodar a aplicação usando o Gunicorn em produção
# O padrão 'wsgi:application' aponta para o arquivo wsgi.py e a variável 'application'
CMD ["gunicorn", "--bind", "0.0.0.0:5002", "wsgi:application"]
