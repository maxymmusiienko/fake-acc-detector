FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    wget \
    build-essential \
    cmake \
    gperf \
    zlib1g-dev \
    libssl-dev \
    libreadline-dev \
    libconfig++-dev \
    libx11-dev \
    libexpat1-dev \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --depth=1 https://github.com/tdlib/td.git /opt/tdlib && \
    mkdir /opt/tdlib/build && cd /opt/tdlib/build && \
    cmake -DCMAKE_BUILD_TYPE=Release .. && \
    cmake --build . --target install -j$(nproc)

ENV LD_LIBRARY_PATH=/usr/local/lib

COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

COPY . /app
WORKDIR /app

CMD ["python3", "test.py"]
