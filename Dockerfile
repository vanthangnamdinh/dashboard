#Using official Python 3.11.7 image
FROM python:3.11.7-slim

# Ip address of the host machine
ENV HTTP_PROXY=    

# Ip address of the host machine
ENV HTTPS_PROXY=    

# Ip address of the host machine
ENV http_proxy=    

# Set working directory in container
WORKDIR /app
# Copy the entire current project to the /app folder in the image
COPY . /app
# Install the necessary packages to create a virtual environment and compile poetry
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*
# Create virtual environment in /app/venv directory
RUN python -m venv /app/venv

# Activate venv and install pip, setuptools, poetry, then install dependencies and run alembic

RUN . /app/venv/bin/activate && \
    pip install --upgrade pip setuptools && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install

ENV HTTP_PROXY=

ENV HTTPS_PROXY=

ENV http_proxy=