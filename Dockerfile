# Use official Python 3.11 slim image for minimal footprint
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LOG_LEVEL=INFO

# Create a non-root user and group
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Ensure the logs directory exists and is owned by the non-root user
RUN mkdir -p logs && chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Start the application
CMD ["python", "main.py"]
