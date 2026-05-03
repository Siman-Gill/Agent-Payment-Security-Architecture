FROM python:3.11-slim

# Install system dependencies for Post-Quantum Cryptography
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Expose API and Dashboard ports
EXPOSE 8000
EXPOSE 8501
