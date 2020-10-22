from ubuntu
ENV DEBIAN_FRONTEND noninteractive
run apt-get update -y
run apt-get install software-properties-common -y
run apt-get install python3.7 -y
copy testfile.py /
entrypoint ["python3", "/testfile.py"]
