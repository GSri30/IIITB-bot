FROM python:3.8-slim-buster

LABEL maintainer="g.sriharsha@iiitb.org"

WORKDIR /bot
COPY . /bot

RUN pip install pipenv
RUN cd /bot && pipenv lock --keep-outdated -r > requirements.txt
RUN pip install -r /bot/requirements.txt

ENTRYPOINT [ "python3","Main.py" ]