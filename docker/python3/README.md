Python 3 images
===============

*pythonboilerplate/python3:latest* image provides a simple Python 3.4 
installation from *debian:jessie* repositories. It includes the Python 
interpreter, pip, python-boilerplate, py.test and invoke. This can be used
as the basis for either a development image or a deploy image.

It assumes that the repository for your application will live on /app/ and its
source code is under /app/src/.


Environment variables 
---------------------

This image defines a few useful variables:

* **PYTHONPATH=/app/src**
  Makes packages in your repository immediately available to the Python interpreter.

* **PYTHON_VERSION=3**
  Version of Python interpreter. This variable is used by some python-boilerplate invoke commands. You should not change it!

* **RUNNING_ON_DOCKER=true**
  Again, used internally in some python-boilerplate invoke commands. Do not change it.

* **WSGI_APPLICATION=test_project.wsgi**
  This variable is used by web applications (e.g. in the pythonboilerplate/python3:django 
  image). We define it here to avoid an extra layer on those images.

* **STATIC_FILES=/var/www/**
  Ditto.
    
    
Specialized images
==================

* **pythonboilerplate/python3:dev**
  Include development packages, Cython and build dependencies for Python. This is usefull if you want to compile packages from 
  source. This image is **much** larger than **python3:latest**. If you need to optimize for image size, consider pulling 
  the dev dependencies manually, compiling your packages and finally cleaning up on a single RUN command.
  
  
* **pythonboilerplate/python3:scipy**
  This image is based on python3:dev and also includes core scientific libraries such as numpy, scipy, sympy, and matplotlib. 
  When executed, this image opens a ipython notebook server on port 8000.
  
      $ docker run -p 8000:8000 pythonboilerplate/python3:scipy
    
    
* **pythonboilerplate/python3:nodejs**
  This image is based on python3:latest and also includes node.js. This is useful in mixed Python/Javascript
  enviroments (usually on web development).
  
      $ docker run -p 8000:8000 pythonboilerplate/python3:scipy
    