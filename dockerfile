FROM ubuntu:16.04

MAINTAINER Josh Lee "jp@joshlee.cc"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev libmysqlclient-dev

ADD ./requirements.txt /app/requirements.txt

ADD . /app

WORKDIR /app

RUN source env/bin/activate

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN export FLASK_APP=shortener

CMD [ "flask run" ]