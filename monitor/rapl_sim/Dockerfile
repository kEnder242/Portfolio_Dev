FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN pip install prometheus_client

# Copy source
COPY app.py .

# Run unbuffered so logs show up immediately
CMD ["python", "-u", "app.py"]
