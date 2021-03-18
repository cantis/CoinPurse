FROM python:3.8-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ENV FLASK_APP="wsgi.py"

RUN pip install --upgrade pip

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt