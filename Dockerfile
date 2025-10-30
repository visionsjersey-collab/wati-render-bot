# Use stable Python 3.10
FROM python:3.10-slim

# Prevent Python from writing .pyc and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install OS dependencies
RUN apt-get update && apt-get install -y curl g++ && \
    pip install --upgrade pip setuptools wheel

# Copy project files
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m playwright install --with-deps chromium

COPY . .

# Run your script
CMD ["python", "main.py"]
