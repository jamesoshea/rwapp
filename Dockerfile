FROM python:3.7.3-alpine3.9

RUN apk add build-base python-dev py-pip jpeg-dev zlib-dev openrc gettext
ENV LIBRARY_PATH=/lib:/usr/lib

COPY app/requirements.txt app/requirements.txt
RUN pip install -r app/requirements.txt

COPY app /app
COPY gunicorn/gunicorn.service /etc/systemd/system/gunicorn.service

WORKDIR /app
RUN python manage.py collectstatic --noinput
RUN mkdir locale
RUN django-admin compilemessages
