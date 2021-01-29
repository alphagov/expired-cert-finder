FROM python:3.8.7-slim-buster

WORKDIR /work

RUN apt-get update && \
    apt-get install -y faketime && \
    apt-get clean

COPY . .

RUN pip install -r requirements.txt && pip install -r requirements_dev.txt

CMD [ "behave" ]