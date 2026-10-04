FROM python:3.11-slim

RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Cria o usuário e a pasta onde o banco SQLite vai residir
RUN useradd -m appuser && mkdir -p /app/data && chown -R appuser:appuser /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Garante a permissão de escrita no banco de dados para o appuser
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 5001

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "4", "wsgi:application"]
