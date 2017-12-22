# This is a base docker image suitable for Python web development. It includes
# node.js and gunicorn.

FROM pythonboilerplate/python3:nodejs


# Install dependencies

RUN apt-get update &&\
    apt-get install --no-install-recommends --no-install-suggests -y \
            nginx &&\
    \
    # Pip dependencies
    pip3 install \
            gunicorn &&\
    \
    # Make a symbolic links to static files and media roots
    ln -s /app/collect/media /var/www/media &&\
    ln -s /app/collect/static /var/www/static &&\
    ln -s /etc/python-boilerplate/tasks.py /app/tasks.py &&\
    \
    # Remove apt and pip caches
    rm ~/.pip/cache/ -rfv &&\
    rm -rf /var/lib/apt/lists/*


# Copy all required files and configure ports and entry point

ENTRYPOINT ["inv", "-r" , "/etc/python-boilerplate/"]
CMD ["start"]
COPY files/ /

