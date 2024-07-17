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

# Install PyTorch with CUDA support
RUN pip install torch --extra-index-url https://download.pytorch.org/whl/cu122

# Install Hugging Face libraries and other required packages
RUN pip install transformers datasets accelerate
RUN pip install scikit-learn
# Create a verification script
RUN echo "#!/bin/bash\n\
echo 'PyTorch version:' \$(python3 -c \"import torch; print(torch.__version__)\")\n\
echo 'CUDA available:' \$(python3 -c \"import torch; print(torch.cuda.is_available())\")\n\
echo 'Transformers version:' \$(python3 -c \"import transformers; print(transformers.__version__)\")\n\
echo 'Datasets version:' \$(python3 -c \"import datasets; print(datasets.__version__)\")\n\
echo 'Accelerate version:' \$(python3 -c \"import accelerate; print(accelerate.__version__)\")\n\
echo 'Locale settings:' \$(locale)\n" > verify.sh

# Make the script executable
RUN chmod +x verify.sh

# Ensure the container runs interactively with Korean locale and executes the verification script
CMD ["bash", "-c", "export LC_ALL=ko_KR.UTF-8 && ./verify.sh && exec bash"]

