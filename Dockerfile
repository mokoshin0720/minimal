FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /development/minimalist

ADD requirements.txt /development/minimalist

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.8.0/wait /wait
RUN chmod +x /wait

RUN pip install -r requirements.txt

ADD . /development/minimalist