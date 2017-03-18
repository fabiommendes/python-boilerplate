# We base on debian:stretch-slim instead of python:3.5 in order to use the
# Python version found on apt. This makes the container lighter, but the Python
# version is not the most up-to-date. Child containers may also benefit
# from using the Python version on apt since they can use binary packages
# without the hassle of installing a C compiler and all the python-dev stack.
FROM debian:stretch-slim

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
            python3-setuptools \
            python3-wheel \
            python3-pytest \
            python3-pytest-cov \
            python3-jinja2 \
            python3-unidecode &&\
    rm -rf /var/lib/apt/lists/*


# Install python-boilerplate from pip

RUN pip3 install python-boilerplate &&\
    rm ~/.pip/cache -rf


# You should install everything under the /app/ directory

WORKDIR /app/
