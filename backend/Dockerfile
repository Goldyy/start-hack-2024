# pull official base image
FROM python:3.11.4  

# set work directory
ENV APP_HOME=/usr/src/app
WORKDIR $APP_HOME

RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/media
RUN mkdir $APP_HOME/shared-data

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1

# install dependencies
RUN apt update 
RUN pip install --upgrade pip
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY .env .env

# copy project
COPY backend/src .