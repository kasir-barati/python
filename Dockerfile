FROM python:3.12.9-bullseye

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD uvicorn src.main:app --host 0.0.0.0 --port $APP_PORT --log-level error
