# This image has Python3 and Nodejs. This is useful for a mixed web development
# with a python/javascript stack
FROM pythonboilerplate/python3


# Install Node.js and npm from binary archive
# (the version found in apt is too old).
RUN curl -SLO "https://nodejs.org/dist/v4.5.0/node-v4.5.0-linux-x64.tar.gz" &&\
    tar -xf "node-v4.5.0-linux-x64.tar.gz" -C /usr/local --strip-components=1 &&\
    rm "node-v4.5.0-linux-x64.tar.gz" -f &&\
    ln -s /usr/local/bin/node /usr/local/bin/nodejs    
