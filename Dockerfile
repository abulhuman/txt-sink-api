# Use the official Ubuntu Focal image from the Docker Hub
FROM ubuntu:noble-20241118.1

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install dependencies
RUN apt update && apt upgrade -y && \
  apt install -y software-properties-common && \
  add-apt-repository ppa:deadsnakes/ppa && \
  apt update && \
  apt install -y python3.12 python3.12-venv pipx python3-pip pkg-config libmysqlclient-dev

# Install Poetry
RUN pipx install poetry==1.8.5 
RUN pipx ensurepath &&\ 
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# Copy only the necessary files for dependency installation
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN  /root/.local/bin/poetry install --no-root

# Copy the rest of the project files
COPY . /app/

RUN /root/.local/bin/poetry run python3 -m pip install uvicorn-worker

# Expose port 80
EXPOSE 80

# Set up the entrypoint
COPY scripts/docker.entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]