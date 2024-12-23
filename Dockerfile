# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install dependencies
RUN set -xe && \
  apt-get update && \
  apt-get install -y --no-install-recommends build-essential && \
  python -m pip install virtualenvwrapper poetry==1.8.5

# Clean up APT when done
RUN apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# Install Uvicorn and Gunicorn
RUN python -m pip install uvicorn uvicorn-worker gunicorn

# Copy only the necessary files for dependency installation
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN poetry install --no-root

# Copy the rest of the project files
COPY . /app/

# Expose port 80
EXPOSE 80

# Set up the entrypoint
COPY scripts/docker.entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]