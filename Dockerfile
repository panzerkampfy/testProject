# pull official base image
FROM python:3.8-slim

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy docker-entrypoint.sh
COPY ./docker-entrypoint.sh ./docker-entrypoint.sh

# copy project
COPY . .

ENTRYPOINT [ "/usr/src/app/docker-entrypoint.sh" ]