FROM python:3.12-bullseye

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y gettext

WORKDIR /code

COPY . .

RUN pip install poetry && poetry install && chmod 755 /code/start-django.sh

CMD ["/code/start-django.sh"]
