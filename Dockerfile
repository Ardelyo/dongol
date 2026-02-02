# DONGOL Docker Image
# Made in Indonesia 🇮🇩

FROM python:3.11-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
COPY requirements-dev.txt .

# Install Python packages
RUN pip install --user --no-cache-dir -r requirements.txt
RUN pip install --user --no-cache-dir -r requirements-dev.txt

# Production stage
FROM python:3.11-slim

LABEL maintainer="Ardellio Satria Anindito <contact@dongol.io>"
LABEL description="DONGOL - Distributed Orchestration System"
LABEL country="Indonesia"
LABEL version="0.1.0"

# Set environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH=/root/.local/bin:$PATH

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Set working directory
WORKDIR /app

# Copy application
COPY . /app/

# Install DONGOL
RUN pip install --no-cache-dir -e ".[all]"

# Create config directory
RUN mkdir -p /root/.dongol

# Expose API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD dongol status || exit 1

# Default command
CMD ["dongol", "--help"]

# Entry point for API server
# docker run -p 8000:8000 dongol/dongol dongol-server
