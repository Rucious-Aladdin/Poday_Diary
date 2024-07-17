FROM python:3.10.2-slim

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    python3-dev \
    git \
    vim \
    net-tools \
    iperf3 \
    locales \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

RUN locale-gen ko_KR.UTF-8
ENV LANG=ko_KR.UTF-8
ENV LANGUAGE=ko_KR:ko
ENV LC_ALL=ko_KR.UTF-8

RUN python3 -m pip install --upgrade pip
RUN pip install flask openai ipython
ADD . /app

ENTRYPOINT python3 app.py