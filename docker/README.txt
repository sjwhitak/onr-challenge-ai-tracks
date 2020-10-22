cd to docker directory
sudo docker build . -t onr-image

sudo docker run -it onr-image
or
sudo docker run onr-image arg1 arg2 arg3...

testfile.py is set up in the container to automatically receive and echo back the arguments passed to docker run.

