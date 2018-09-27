FROM node:10.11.0-alpine as frontend
WORKDIR /usr/src/app
COPY . ./
RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh
RUN ./frontend.sh

FROM python:2.7.15-alpine
WORKDIR /usr/src/app
COPY config *.sh .env ./
COPY requirements ./requirements
COPY cfgov ./cfgov
ADD  https://bootstrap.pypa.io/get-pip.py ./get-pip.py
RUN set -ex \
    && apk update && apk upgrade \
    && apk add --no-cache \
            gcc \
            make \
            bash \
            libc-dev \
            musl-dev \
            linux-headers \
            zlib-dev \
            libxml2-dev \
            libxslt-dev \
            libffi-dev \
            jpeg-dev \
            pcre-dev \
            postgresql-dev \
            postgresql-client \
    && python ./get-pip.py && pip install -r ./requirements/local.txt
COPY --from=frontend /usr/src/app/cfgov/static_built /usr/src/app/cfgov/static_built
RUN ./setup.sh docker
