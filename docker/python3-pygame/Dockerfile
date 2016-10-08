FROM pythonboilerplate/python3

RUN apt-get update &&\
    apt-get install --no-install-recommends --no-install-suggests -y \
            build-essential \
            python3-dev \
            python3-numpy \
            libsmpeg-dev \
            libportmidi-dev \
            libavformat-dev \
            libswscale-dev \
            libjpeg-dev \
            libfreetype6-dev \
            libsdl-dev \
            libsdl-image1.2-dev \
            libsdl-mixer1.2-dev \
            libsdl-ttf2.0-dev \
            libsmpeg0 \
            libportmidi0 \
            libavformat56 \
            libswscale3 \
            libjpeg62-turbo \
            libfreetype6 \
            libsdl1.2debian \
            libsdl-image1.2 \
            libsdl-mixer1.2 \
            libsdl-ttf2.0 \
            mercurial &&\
    \
echo "relax"
RUN \
    # Clone mercurial repo and build
    hg clone https://bitbucket.org/pygame/pygame &&\
    cd pygame &&\
echo "relax"
RUN \
    cd pygame &&\
    python3 setup.py build &&\
    python3 setup.py install &&\
    cd .. &&\
    \
echo "relax"
RUN \
    # Remove unnecessary files
    rm pygame -rf &&\
    apt-get remove -yf \
            build-essential \
            libsmpeg-dev \
            libportmidi-dev \
            libavformat-dev \
            libswscale-dev \
            libjpeg-dev \
            libfreetype6-dev \
            libsdl-dev \
            libsdl-image1.2-dev \
            libsdl-mixer1.2-dev \
            libsdl-ttf2.0-dev \
            mercurial &&\
    apt-get autoremove -yf &&\
    rm -rf /var/lib/apt/lists/*
