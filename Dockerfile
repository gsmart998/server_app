FROM python:3.12

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

ENV PORT 8000
ENV HOST "0.0.0.0"
ENV DB_PATH "database/sqlite_base.db"

COPY . /usr/src/app/
RUN pip install --no-cache-dir --progress-bar off -r requirements.txt

EXPOSE 8000

CMD [ "python", "main.py" ]