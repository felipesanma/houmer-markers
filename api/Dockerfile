# syntax=docker/dockerfile:1

FROM python:3.9-slim

WORKDIR /app

COPY /requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

EXPOSE 8080

COPY . .

CMD ["python", "app.py"]

