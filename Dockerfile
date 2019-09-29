FROM python:3.6.7-stretch

RUN mkdir app

ADD . app

RUN pip3 install -r app/requirements.txt

WORKDIR app

CMD ["python","server.py"]
