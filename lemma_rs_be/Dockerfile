FROM python:3.8.0

WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV ENV_PATH .env.dev.live


RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean


RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt







