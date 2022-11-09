FROM python:3.9-alpine3.15

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#RUN apk add --update netcat

EXPOSE 8000

# install dependencies
RUN pip install --upgrade pip


COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .

# copy project
COPY . .

ENTRYPOINT ./entrypoint.sh