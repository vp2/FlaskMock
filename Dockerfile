FROM python:2

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./requirements.txt /opt/FlaskMock/requirements.txt

WORKDIR /opt/FlaskMock

RUN pip install -r requirements.txt

COPY . /opt/FlaskMock
RUN chmod a+x boot.sh

EXPOSE 5000

VOLUME /opt/FlaskMock

ENV FLASK_APP flaskmock.py
ENTRYPOINT ["./boot.sh"]