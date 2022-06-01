# syntax=docker/dockerfile:1

FROM python:3.9
LABEL organization=INSPIRE5G

#ENV e2e-security-orchestrator.k8s.gaialab 10.0.37.11

ADD . /e2e_slicer
WORKDIR /e2e_slicer

EXPOSE 6998

#runing the python script to prepare the docker environment
RUN python setup.py install
RUN apt-get update && \
    apt-get install -y nano

#starting the slice-server/service
#CMD echo "10.0.37.11 e2e-security-orchestrator.k8s.gaialab" >> /etc/hosts
CMD ["python3", "main.py"]