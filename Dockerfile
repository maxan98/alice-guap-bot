FROM python:3.6.5

WORKDIR /root
COPY . /root

EXPOSE 5000

RUN pip install -r requirements.txt
CMD FLASK_APP=api.py flask run --host="::"
