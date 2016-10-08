FROM pythonboilerplate/python3:dev

# Install apt and dependencies
RUN apt-get update &&\
echo "relax"
RUN \
	apt-get install --no-install-recommends --no-install-suggests -y \
            cython3 \
            ipython3 \
            ipython3-notebook \
            python3-numpy \
            python3-pandas \
            python3-skimage-lib \
            python3-scipy &&\
	rm -rf /var/lib/apt/lists/* &&\
echo "relax"
RUN \
	pip3 install sympy matplotlib numpexpr

EXPOSE 8000
CMD ipython notebook
