# This image has django, gunicorn, nodejs, npm, webpack, and sass.
# Child containers can override the Django version by specifying it during
# pip installation. We install a Django app for convenience so the base
# image always have something to show.

# This image has Python3 and Nodejs with npm and webpack. This is useful for
# mixed web development with a python/javascript stack

FROM pythonboilerplate/python3


# Install Node.js and npm from binary archive
# (the version found in apt is too old).
RUN curl -SLO "https://nodejs.org/dist/v4.5.0/node-v4.5.0-linux-x64.tar.gz" &&\
    tar -xf "node-v4.5.0-linux-x64.tar.gz" -C /usr/local --strip-components=1 &&\
    rm "node-v4.5.0-linux-x64.tar.gz" -f &&\
    ln -s /usr/local/bin/node /usr/local/bin/nodejs &&\
    \
    # Install webpack globally
    npm install \
            node-sass \
            webpack \
            webpack-dev-server -g &&\
    \
    # Local installations of the same packages
    npm link \
        node-sass \
        webpack \
        webpack-dev-server &&\
    \
    # Install local npm modules. These go under /app/node_modules/
    npm install \
            css-loader \
            style-loader \
            sass-loader \
            extract-text-webpack-plugin \
            babel-core \
            babel-preset-es2015 &&\
    \
    npm cache clean
