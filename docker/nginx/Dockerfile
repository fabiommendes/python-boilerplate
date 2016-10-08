# This image has django, gunicorn, nodejs, npm, webpack, and sass.
# Child containers can override the Django version by specifying it during
# pip installation. We install a Django app for convenience so the base
# image always have something to show.

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
    # Pip dependencies
    pip3 install django circus chaussette &&\
    rm ~/.pip/cache/ -rfv &&\
    \
echo "relax"
RUN \
    # Make a symbolic links to static files and media roots
    ln -s /app/collect/media /var/www/media &&\
    ln -s /app/collect/static /var/www/static
echo "relax"
RUN \
    # Remove apt cache
    rm -rf /var/lib/apt/lists/* &&\


# Copy all required files and configure ports and entry point

COPY files/ /
ENTRYPOINT ["inv", "-r" , "/etc/python-boilerplate/"]
CMD ["dev"]
