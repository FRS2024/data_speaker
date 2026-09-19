# Use an official lightweight Python 3.12 image
FROM python:3.12-slim

# Prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SANDBOX_HOST=0.0.0.0 \
    SANDBOX_PORT=8000 \
    SANDBOX_TIMEOUT=60 \
    PYTHONPATH=/app

# Install system dependencies (curl for container healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create a non-privileged user and group (UID/GID 1000)
RUN groupadd -g 1000 appgroup && \
    useradd -u 1000 -g appgroup -m -s /bin/bash appuser

WORKDIR /app

# Upgrade pip and install the complete Modern Core Data Stack
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    fastapi==0.111.0 \
    "uvicorn[standard]==0.30.1" \
    pydantic==2.7.4 \
    ipython==8.25.0 \
    pandas==2.2.2 \
    polars==0.20.31 \
    pyarrow==16.1.0 \
    numpy==1.26.4 \
    scipy==1.13.1 \
    scikit-learn==1.5.0 \
    statsmodels==0.14.2 \
    plotly==5.22.0 \
    matplotlib==3.9.0 \
    seaborn==0.13.2 \
    openpyxl==3.1.4 \
    tabulate==0.9.0 \
    httpx==0.27.0

# Copy application source code
COPY . /app/services/sandbox

# Set permissions for non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root execution
USER appuser

EXPOSE 8000

# Container healthcheck
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start the sandbox FastAPI execution daemon
CMD ["uvicorn", "services.sandbox.server:app", "--host", "0.0.0.0", "--port", "8000"]
