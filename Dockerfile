FROM python:3.9-slim

ARG USERNAME
ARG PASSWORD

ENV BASIC_AUTH_USERNAME=$USERNAME
ENV BASIC_AUTH_PASSWORD=$PASSWORD

WORKDIR /usr

COPY ./requirements.txt /usr/requirements.txt

RUN pip3 install -r requirements.txt

COPY ./src /usr/src
COPY ./models /usr/models

ENTRYPOINT [ "python3" ]

CMD [ "src/app/main.py" ]