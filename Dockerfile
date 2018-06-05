FROM python:3.6.5

WORKDIR /root
COPY . /root

EXPOSE 443

RUN pip install -r requirements.txt
CMD pyrhon3 run.py
