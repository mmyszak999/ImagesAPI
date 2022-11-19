FROM python:3.11.0-slim-buster

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install virtualenv

COPY --from=initial-stage /initial/requirements.txt /app/requirements.txt

RUN virtualenv venv \
    && . venv/bin/activate \
    && pip install --no-cache-dir --upgrade -r /app/requirements.txt \
    && pip install psycopg2 

COPY ./config/.env.template ./config/.env

COPY . .

ENTRYPOINT ["python3", "manage.py", "runserver", "0.0.0.0:8000"]