# Use Python 3.11 slim image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p /app/test_history \
    && mkdir -p /app/reports \
    && mkdir -p /app/reports/graphs \
    && mkdir -p /app/image

# Copy application code
COPY app.py .
COPY locustfile.py .
COPY image/logo.png ./image/logo.png 2>/dev/null || true

# Create startup script with better error handling
RUN echo '#!/bin/bash\n\
set -e\n\
echo "=========================================="\n\
echo "🚀 Starting EAII Performance Testing Tool"\n\
echo "=========================================="\n\
echo "📊 Streamlit will run on port: $PORT"\n\
echo "🦗 Locust will run on port: ${LOCUST_PORT:-8089}"\n\
echo "=========================================="\n\
\n\
# Start Locust in background with logging\n\
echo "Starting Locust..."\n\
locust -f locustfile.py --host=http://localhost --web-port ${LOCUST_PORT:-8089} --web-host 0.0.0.0 --headless &\n\
LOCUST_PID=$!\n\
echo "✅ Locust started with PID: $LOCUST_PID"\n\
\n\
# Wait for Locust to be ready\n\
echo "Waiting for Locust to be ready..."\n\
for i in {1..10}; do\n\
    if curl -s http://localhost:${LOCUST_PORT:-8089} > /dev/null; then\n\
        echo "✅ Locust is ready!"\n\
        break\n\
    fi\n\
    echo "Waiting... ($i/10)"\n\
    sleep 2\n\
done\n\
\n\
# Start Streamlit\n\
echo "Starting Streamlit..."\n\
streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.enableCORS false --server.enableXsrfProtection false\n\
' > /app/start.sh && chmod +x /app/start.sh

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV LOCUST_PORT=8089
ENV RENDER=true

# Expose ports
EXPOSE 8080 8089

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/ || exit 1

# Run the startup script
CMD ["/app/start.sh"]
