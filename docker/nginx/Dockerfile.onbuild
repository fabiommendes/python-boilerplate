# This image should be used with docker-compose in a multi-container
# configuration in which nginx serves stactic files and comunicates with another
# container on port 8080 that serves dynamic content using the wsgi interface.
#
FROM nginx:1.11


# Nginx config

ADD nginx.conf /etc/nginx/nginx.conf
VOLUME ["/sock/"]
ONBUILD ADD collect/ /var/www/