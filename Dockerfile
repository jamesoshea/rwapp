FROM python:3.7.3-alpine3.9

COPY app /app
COPY gunicorn/gunicorn.service /etc/systemd/system/gunicorn.service
COPY nginx/rwapp /etc/nginx/sites-available/rwapp
WORKDIR /app

RUN apk add build-base python-dev py-pip jpeg-dev zlib-dev openrc
ENV LIBRARY_PATH=/lib:/usr/lib

RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput