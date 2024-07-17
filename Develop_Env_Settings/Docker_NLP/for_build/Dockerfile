# Base image with CUDA 12.2 and cuDNN 8
FROM nvidia/cuda:12.2.0-devel-ubuntu22.04

# Set the working directory
WORKDIR /workspace

# Install necessary dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    python3-dev \
    git \
    vim \
    net-tools \
    iperf3 \
    locales \
    && rm -rf /var/lib/apt/lists/*

# Configure locales
RUN locale-gen ko_KR.UTF-8
ENV LANG=ko_KR.UTF-8
ENV LANGUAGE=ko_KR:ko
ENV LC_ALL=ko_KR.UTF-8

# Upgrade pip
RUN python3 -m pip install --upgrade pip

# Install Flask and other necessary Python packages
RUN pip install flask torch transformers

# Copy the server script and roberta script into the container
COPY server.py /workspace/server.py
COPY roberta.py /workspace/roberta.py

# Set environment variables for Flask
ENV FLASK_APP=server.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port Flask is running on
EXPOSE 5000

# Run the Flask server
CMD ["flask", "run"]

