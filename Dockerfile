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

CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn -b 0.0.0.0:8000 api.wsgi"]

EXPOSE 8000
