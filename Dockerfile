FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --progress-bar off -r requirements.txt

COPY /src .