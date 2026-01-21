FROM python:3.12-slim AS base
WORKDIR /app
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc make \
    && rm -rf /var/lib/apt/lists/*
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser
COPY requirements.txt .

FROM base AS development
COPY requirements.dev.txt .
RUN pip install --no-cache-dir -r requirements.dev.txt -r requirements.txt
CMD ["make", "start_dev"]

FROM base AS production
RUN pip install --no-cache-dir -r requirements.txt
COPY Makefile .
COPY src/ ./src/
CMD ["make", "start"]
