FROM python:3.11.9-alpine3.19

RUN apk update && apk add --no-cache ffmpeg git

WORKDIR /app
COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

RUN git clone https://github.com/polygon/spectrum_painter.git /opt/spectrum_painter \
&& cd /opt/spectrum_painter && pip install --user -e .

COPY img2iqstream.py /opt/spectrum_painter/spectrum_painter/img2iqstream.py
COPY spectrum_painter.py /opt/spectrum_painter/spectrum_painter/spectrum_painter.py

ENV PYTHONPATH=/app
