FROM python:3.12

WORKDIR /app

COPY /src .

RUN pip install --no-cache-dir --progress-bar off -r requirements.txt