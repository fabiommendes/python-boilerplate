# Python 3 images
docker build . -f dockerfile-python3 -t pythonboilerplate/python3
docker build . -f dockerfile-scientific-3 -t pythonboilerplate/python3:scientific
docker build . -f dockerfile-games-3 -t pythonboilerplate/python3:games

sed 's/python3/python/' dockerfile-python3 > dockerfile-python2
sed 's/python3/python/' dockerfile-scientific-3 > dockerfile-scientific-2
sed 's/python3/python/' dockerfile-games-3 > dockerfile-games-2
docker build . -f dockerfile-python2 -t pythonboilerplate/python2
docker build . -f dockerfile-scientific-2 -t pythonboilerplate/python2:scientific
docker build . -f dockerfile-games-2 -t pythonboilerplate/python2:games


docker push pythonboilerplate/python3
docker push pythonboilerplate/python2
docker push pythonboilerplate/python3:scientific
docker push pythonboilerplate/python2:scientific
docker push pythonboilerplate/python3:games
docker push pythonboilerplate/python2:games
