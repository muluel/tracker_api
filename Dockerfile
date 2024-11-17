FROM python:3.13-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk update
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY poetry.lock /app
COPY pyproject.toml /app
COPY ./api /app

RUN poetry install