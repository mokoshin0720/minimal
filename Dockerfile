FROM python:3

ARG SECRET_KEY
RUN echo $SECRET_KEY

ARG TEST
RUN echo $TEST

ENV TEST=$TEST
RUN echo $TEST

ARG AWS_ACCESS_KEY_ID
RUN echo $AWS_ACCESS_KEY_ID

ARG AWS_SECRET_ACCESS_KEY
RUN echo $AWS_SECRET_ACCESS_KEY

ARG AWS_STORAGE_BUCKET_NAME
RUN echo $AWS_STORAGE_BUCKET_NAME

RUN set

WORKDIR /development/minimalist

ADD requirements.txt /development/minimalist

RUN pip install -r requirements.txt

ADD . /development/minimalist

RUN ls

RUN python manage.py collectstatic --noinput

COPY . .
CMD ["web:", "gunicorn", "minimalist.wsgi"]