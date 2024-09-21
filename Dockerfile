# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Optional: Unbuffered output for immediate logging
ENV PYTHONUNBUFFERED=1

# Copy the requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the backend code
COPY . .

# Expose the port for Prometheus metrics
EXPOSE 8001

# Run the backend
CMD ["python", "main.py"]
