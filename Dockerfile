FROM python:3.12

ENV PYTHONDONTWRITEBYCODE=1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple 

EXPOSE 8000
COPY . . 