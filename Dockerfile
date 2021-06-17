FROM python:3.7
RUN apt-get update -y
RUN apt-get install -y xpdf

COPY ./app/requirements.txt /usr/src/app/requirements.txt
RUN pip install -r /usr/src/app/requirements.txt

COPY ./app /usr/src/app

