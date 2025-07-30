FROM python:3.12.9-bullseye AS base

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

EXPOSE $APP_PORT

FROM base AS dev

CMD make start_dev

FROM base AS prod

COPY Makefile .
COPY . .

CMD make start
