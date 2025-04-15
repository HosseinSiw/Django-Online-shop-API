FROM python:3.12

ENV PYTHONDONTWRITEBYCODE=1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000
COPY . . 