# Pi-5 Relay Controller Docker Image
# ==================================
# For containerized deployment (advanced users)

FROM python:3.11-slim-bullseye

# Metadata
LABEL maintainer="Pi-5 Relay Controller"
LABEL description="Modern web-based relay controller for Raspberry Pi 5"
LABEL version="1.0.0"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgpiod2 \
    libgpiod-dev \
    gpiod \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 relay && \
    chown -R relay:relay /app

# Switch to non-root user
USER relay

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/status/1 || exit 1

# Run application
CMD ["python", "server.py"]
