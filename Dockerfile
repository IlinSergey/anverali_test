FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade setuptools
RUN pip install --no-cache-dir -r requirements.txt

COPY src /app/src
