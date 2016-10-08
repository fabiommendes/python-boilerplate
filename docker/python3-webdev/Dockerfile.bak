FROM pythonboilerplate/python3:nodejs


# Install dependencies

RUN apt-get update &&\
echo "relax"
RUN \
    apt-get install --no-install-recommends --no-install-suggests -y \
            python3-zmq \
            nginx &&\
    \
echo "relax"
RUN \
    apt-get install --no-install-recommends --no-install-suggests -y \
            python3-tornado \
            python3-psutil &&\
    \
echo "relax"
RUN \
    # Pip dependencies
    pip3 install \
        chaussette \
        circus \
        gunicorn \
        unix &&\
    rm ~/.pip/cache/ -rfv &&\
    \
echo "relax"
RUN \
    # Make a symbolic links to static files and media roots
    ln -s /app/collect/media /var/www/media &&\
    ln -s /app/collect/static /var/www/static &&\
    \
echo "relax"
RUN \
    # Remove apt cache
    rm -rf /var/lib/apt/lists/*


# Env (until we update python3 image)
ENV WSGI_APPLICATION=app

# Copy all required files and configure ports and entry point

COPY files/ /
ENTRYPOINT ["inv", "-r" , "/etc/python-boilerplate/"]
CMD ["start"]
