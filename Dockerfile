FROM python:3.12

WORKDIR /app

ENV PORT 8000
ENV HOST "0.0.0.0"
ENV USERNAME="admin"
ENV PASSWORD="password"
ENV DB_HOST="localhost"
ENV DB_PORT="5432"
ENV DATABASE="pg_db"

COPY . .

RUN pip install --no-cache-dir --progress-bar off -r requirements.txt

EXPOSE 8000

CMD [ "python", "main.py" ]