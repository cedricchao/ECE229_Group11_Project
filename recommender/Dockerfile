FROM python:3.6 as base

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app
ENV PYTHONPATH ..
CMD ["uvicorn","recommender.asgi:app","--host","0.0.0.0"] 

