FROM alpine:3.7

RUN apk update && \
    apk add py2-pip

RUN pip install --upgrade pip

COPY ./requirements.txt /opt/FlaskMock/requirements.txt

WORKDIR /opt/FlaskMock

RUN pip install -r requirements.txt

COPY . /opt/FlaskMock
RUN chmod a+x boot.sh

EXPOSE 5000

VOLUME /opt/FlaskMock

ENV FLASK_APP flaskmock.py
ENTRYPOINT ["./boot.sh"]