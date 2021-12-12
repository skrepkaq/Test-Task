FROM python:3.10.0
ENV PYTHONUNBUFFERED 1
RUN mkdir /src
WORKDIR /src
COPY requirements.txt /src/
COPY wait-for-it.sh /
RUN pip install -r requirements.txt
COPY src .