# syntax=docker/dockerfile:1.4
ARG PYTHON_VERSION=3.13.2
FROM python:${PYTHON_VERSION}-slim-bullseye as base

ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.8.0

WORKDIR /code

RUN pip install poetry==${POETRY_VERSION}

COPY ./pyproject.toml pyproject.toml
COPY ./poetry.lock poetry.lock

RUN poetry export -f requirements.txt --output requirements.txt --with test --without-hashes
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

COPY . /code

ENTRYPOINT ["python3"]
CMD ["run.py"]
