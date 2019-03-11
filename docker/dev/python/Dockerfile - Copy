FROM python:3.6

COPY ./app /app

WORKDIR /app

RUN pip install -r requirements/dev_requirements.txt

COPY ./docker/dev/python/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["sh","/entrypoint.sh"]