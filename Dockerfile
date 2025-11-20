# ===============================
# 🧱 Etapa base
# ===============================
FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ===============================
# 🐍 Instalar dependências do projeto
# ===============================
RUN pip install uv

COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev

COPY . .


# ===============================
# ⚙️ Variáveis de ambiente
# ===============================
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/usr/local/bin:${PATH}"

# ===============================
# 🚀 Comando padrão (teste)
# ===============================
CMD ["uv", "run", "python", "run.py"]
