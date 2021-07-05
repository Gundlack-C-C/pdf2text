FROM python:3.7-slim-buster
RUN apt-get update -y
RUN apt-get install -y xpdf

COPY ./app /usr/src/app
COPY docker-entrypoint.sh /usr/src/app

WORKDIR /usr/src/app
RUN pip install -r /usr/src/app/requirements.txt

RUN chmod +x ./docker-entrypoint.sh

ENTRYPOINT ["/usr/src/app/docker-entrypoint.sh"]