FROM python:3.11-slim

# Install Node.js v16 and default-jdk (HotSpot JVM)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y --no-install-recommends \
    nodejs \
    gcc \
    g++ \
    default-jdk \
    mono-devel \
    mono-mcs \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy execution service
COPY executor-service.py /app/executor-service.py
COPY requirements.txt /app/requirements.txt

# Create test_cases directory for file-based test cases
RUN mkdir -p /app/test_cases

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user (ACA requirement)
RUN useradd -m -u 1000 executor && \
    chown -R executor:executor /app

USER executor

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Run the service with Gunicorn for concurrent request handling
# Use 4 workers (2 per CPU core) with 2 threads each = 8 concurrent requests per replica
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "2", "--timeout", "60", "--worker-class", "sync", "executor-service:app"]

