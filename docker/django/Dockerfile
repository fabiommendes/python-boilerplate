# We base on debian:jessie instead of python:3.4 to use the Python version found
# on apt. This makes the container lighter. Child containers may also benefit 
# from using apt.
FROM pythonboilerplate/python

ENV GUNICORN_WSGI_APPLICATION=test_project.wsgi
ENV PYTHONPATH=/app/src/

# Install django and gunicorn from pip in order to choose later versions
# Child containers can overide the Django version by specifying it in the 
# install dependencies. We install django for convenience so the base image
# always has an app running.
RUN pip3 install django gunicorn \
    && rm ~/.pip/cache/ -rfv

# Copy gunicorn conf
ADD . /app
WORKDIR /app

# Expose ports
EXPOSE 8000

# Entry point
CMD gunicorn -c /app/gunicorn_conf.py $GUNICORN_WSGI_APPLICATION --reload

