# Stage 1: Builder
FROM python:3.12-slim AS builder

# Copia o binário do uv diretamente de imagem oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copia arquivos de dependência para instalação
COPY pyproject.toml uv.lock ./

# Instala as dependências no .venv local usando uv
RUN uv venv && \
    uv pip install --upgrade pip && \
    uv sync --frozen && \
    uv pip install uvloop

# Stage 2: Runtime
FROM python:3.12-slim

WORKDIR /app

# Copie o arquivo de dependências
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie toda a estrutura do projeto
COPY app.py .
COPY src/ ./src/

# Exponha a porta que o servidor usa
EXPOSE 8015

# Variáveis de ambiente (devem ser fornecidas no runtime)
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Defina o comando para executar quando o container iniciar
CMD ["python", "app.py"]