FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /code/