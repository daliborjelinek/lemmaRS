FROM python:3.8.0

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean



# # copy entrypoint.sh
# COPY ./entrypoint.sh .

# # copy project
COPY . .

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt







