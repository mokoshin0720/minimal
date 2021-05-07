FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /development/minimalist

ADD requirements.txt /development/minimalist

RUN pip install -r requirements.txt

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.6.0/wait /wait
RUN chmod +x /wait

ADD . /development/minimalist

CMD /wait && python manage.py test