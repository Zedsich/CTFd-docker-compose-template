FROM python:3.9-slim-buster

RUN mkdir -p /app
COPY ./templates /app/templates
COPY ./app.py /app/app.py
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app

RUN sed -i "s|http://deb.debian.org/debian|https://mirror.sjtu.edu.cn/debian|g" /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libffi-dev \
        libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* 

RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
