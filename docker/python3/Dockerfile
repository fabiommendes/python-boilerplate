# We base on debian:jessie instead of python:3.4 to use the Python version found
# on apt. This makes the container lighter. Child containers may also benefit 
# from using the Python version on apt since they can use binary packages
# without the hassle of installing a C compiler and all python-dev stack.

FROM debian:jessie

MAINTAINER Fábio Macêdo Mendes <fabiomacedomendes@gmail.com>

ENV PYTHONPATH=/app/src \
    PYTHON_VERSION=3 \
    PYTHON_BOILERPLATE_ACTION=start \
    PYTHON_BOILERPLATE_TASK_DIR=/etc/python-boilerplate/ \
    RUNNING_ON_DOCKER=true \
    WSGI_APPLICATION=app \
    STATIC_FILES=/var/www/


# Install dependencies and create folders

RUN mkdir /app/ &&\
    mkdir /app/src/ &&\
    mkdir /var/www/ &&\
    \
    # Install apt dependencies
    apt-get update &&\
    apt-get install --no-install-recommends --no-install-suggests -y \
            curl \
            python3 \
            python3-pip \
            python3-pytest \
            python3-pytest-cov \
            python3-jinja2 \
            python3-unidecode &&\
    rm -rf /var/lib/apt/lists/* &&\
    \
    # Install python-boilerplate from pip
    pip3 install python-boilerplate &&\
    rm ~/.pip/cache -rf


# You should install everything under the /app/ directory

WORKDIR /app/
