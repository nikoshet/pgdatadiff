FROM alpine:3.10

RUN apk add python3-dev postgresql-dev py3-pip gcc musl-dev git

RUN pip3 install wheel

COPY . .

RUN python3 setup.py sdist bdist_wheel

RUN mv dist /tmp/dist

RUN pip3 install /tmp/dist/*.tar.gz 
