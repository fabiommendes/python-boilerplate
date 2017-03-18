# We base this image on pytonboilerplate/python3 in order to optimize cache
# usage. This image should be chosen by those that need to compile C extensions
# from the source.

FROM pythonboilerplate/python3:latest


# Install apt development dependencies. This image includes Python headers,
# a C compiler and Cython

RUN apt-get update &&\
    apt-get install --no-install-recommends --no-install-suggests -y \
            build-essential \
            python3-dev \
            cython3 &&\
    rm -rf /var/lib/apt/lists/*
