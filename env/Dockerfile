FROM python:3.11.9-alpine3.19

RUN apk update && apk add --no-cache ffmpeg

WORKDIR /app
COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH=/app
