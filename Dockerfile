FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install specific versions of MLflow, MLserver, and the required interface module
RUN pip install --no-cache-dir mlflow==2.11.1 mlserver==1.3.5 mlserver-mlflow==1.3.5

# Copy the generation script into the container
COPY generate_model.py /app/generate_model.py

# Execute the script to build a natively valid MLmodel artifact structure
RUN python /app/generate_model.py

EXPOSE 5000