# Use Python 3.13 slim image for smaller size
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    build-essential \
    libpq-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip, wheel, and setuptools for faster builds
RUN pip install --no-cache-dir --upgrade pip wheel setuptools

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set runtime optimizations
ENV PYTHONUNBUFFERED=1

# Copy application code
COPY . .

# Pre-compile bytecode to reduce startup overhead
RUN python -m compileall -q .

# Run with optimizations enabled
CMD ["python", "-O", "-m", "Sakura"]