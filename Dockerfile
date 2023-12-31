FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.2.2

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev

WORKDIR /code

RUN pip3 install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /code/

RUN poetry install --without dev

COPY . /code/

RUN adduser --disabled-password --no-create-home app

USER app