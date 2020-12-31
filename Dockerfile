# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

# set work directory
WORKDIR /usr/src/app

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
RUN pip install --upgrade pip
ADD requirements.txt .
RUN pip install -r requirements.txt

# copy the project
COPY . /usr/src/app/

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
#CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
