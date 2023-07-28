# Base image
FROM python:3.7-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /doktortg_backend

# Install system dependencies
RUN apt-get update

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .
CMD flask db init ; \
flask db stamp head && \
flask db migrate && \
flask db upgrade && \
gunicorn --workers 2 --timeout 120 -b 0.0.0.0:5000 --reload doktortg:app
