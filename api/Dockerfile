FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# -----------------------
# System deps
# -----------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# -----------------------
# Install uv
# -----------------------
RUN pip install --no-cache-dir --upgrade pip wheel uv

# -----------------------
# Copy dependency files
# -----------------------
COPY pyproject.toml uv.lock* ./

# -----------------------
# Install dependencies
# -----------------------
RUN uv sync --no-dev

# -----------------------
# Copy app source
# -----------------------
COPY ./ ./

# -----------------------
# Expose & run
# -----------------------
EXPOSE 8000

CMD ["uv", "run", "python", "run.py"]
