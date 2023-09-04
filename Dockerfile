# frontend
FROM node:18 AS frontend

WORKDIR /calendar-gen/app

COPY ./app/package.json ./
COPY ./app/package-lock.json ./

RUN npm install

COPY ./app ./

RUN npm run build

# backend 
FROM debian:bookworm

WORKDIR /calendar-gen/backend

RUN apt-get update && \
    apt-get install -y build-essential sqlite3 python3-pip python3-venv

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN apt-get update && \
    apt-get install -y build-essential wget tar

COPY ./backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./backend ./

COPY --from=frontend /calendar-gen/app/build /calendar-gen/backend/build

ENV FLASK_ENV PROD

CMD exec gunicorn wsgi:app --bind 0.0.0.0:$PORT