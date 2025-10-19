# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Install ffmpeg and other system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock* ./
COPY main.py ./
COPY README.md ./

# Install uv for faster dependency management
RUN pip install --no-cache-dir uv

# Install project dependencies
RUN uv pip install --system -r pyproject.toml

# Create a directory for temporary sandbox environments
RUN mkdir -p /tmp/ffmpeg_sandboxes

# Create a directory for persistent storage
RUN mkdir -p /app/data

# Define volume for persisting FFmpeg output files
VOLUME ["/app/data"]

# Expose port (adjust if your app uses a different port)
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "main.py"]
