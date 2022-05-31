FROM python:3.10.1 as base

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app

#FROM test AS build
ENV FLASK_APP main

CMD ["flask", "run","--host","0.0.0.0"]
