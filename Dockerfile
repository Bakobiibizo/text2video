FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy requirements first for better caching
COPY pyproject.toml .

# Install Python dependencies
RUN /root/.local/bin/uv sync

# Copy the rest of the application
COPY . .

# Expose the port
EXPOSE 7095
