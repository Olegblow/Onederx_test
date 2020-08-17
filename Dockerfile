FROM python:3.8

COPY ./requirements.txt requirements.txt

COPY ./app /app

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /app
