# syntax=docker/dockerfile:1

FROM python:3.9
LABEL organization=INSPIRE5G

#RUN apk add --no-cache python2 g++ make

ADD . /e2e_slicer
WORKDIR /e2e_slicer

EXPOSE 6998

#COPY . .

#runing the python script to prepare the docker environment
RUN python setup.py install

#starting the slice-server/service
CMD ["python3", "main.py"]