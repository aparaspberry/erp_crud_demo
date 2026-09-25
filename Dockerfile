# Stage 1: Build dependencies
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Production runtime stage
FROM python:3.11-slim
WORKDIR /app

# Create a non-root system user for security enforcement
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Copy built dependencies from builder stage
COPY --from=builder /root/.local /home/appuser/.local
COPY app.py index.html .

# Grant execution ownership to non-root user
RUN chown -R appuser:appgroup /app
USER appuser

ENV PATH=/home/appuser/.local/bin:$PATH
EXPOSE 5000

# Container health monitoring
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]