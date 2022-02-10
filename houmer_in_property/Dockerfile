# syntax=docker/dockerfile:1

FROM python:3.9-slim

WORKDIR /houmer_in_property

COPY /requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY . .

CMD ["python", "app.py"]