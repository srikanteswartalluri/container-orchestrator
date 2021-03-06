FROM docker:dind
RUN apk add python3

RUN apk add py3-pip
COPY . /
RUN pip install -r /requirements.txt

