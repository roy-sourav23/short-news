# Pull base image
FROM python:3.10.7-slim-bullseye

# set environmental variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTOHNUNBUFFERED 1

# Set working directory
WORKDIR /code

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# COPY PROJECT
COPY . .