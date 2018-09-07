FROM python:3.6

COPY ./app /app

WORKDIR /app

RUN pip install -r requirements/prod_requirements.txt

COPY ./docker/prod/python/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["sh","/entrypoint.sh"]