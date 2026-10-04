# 1. Usa a imagem oficial do Python Slim (Reduzida superfície de ataque para AppSec)
FROM python:3.11-slim

# 2. Comando AppSec: Atualiza as bibliotecas do Debian Slim aplicando patches de segurança contra CVEs locais
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

# 3. Configura variáveis de ambiente otimizadas para o Python rodar em contêineres
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. Define o diretório de trabalho interno
WORKDIR /app

# 5. Copia apenas o requirements primeiro para tirar vantagem do cache de camadas do Docker
COPY requirements.txt .

# 6. Instala as dependências (incluindo o flask-bcrypt) sem salvar arquivos de cache locais
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copia todo o código-fonte do microsserviço para dentro da imagem
COPY . .

# 8. Princípio do Menor Privilégio (AppSec): Cria o appuser e a pasta segura /app/data para o SQLite
RUN useradd -m appuser && mkdir -p /app/data && chown -R appuser:appuser /app

# 9. Muda o contexto de execução de ROOT para o usuário comum sem privilégios administrativos
USER appuser

# 10. Expõe a porta lógica interna configurada para o serviço de usuários
EXPOSE 5002

# 11. Inicializa o servidor de produção rodando com Gunicorn e 4 workers paralelos
CMD ["gunicorn", "--bind", "0.0.0.0:5002", "--workers", "4", "wsgi:application"]
