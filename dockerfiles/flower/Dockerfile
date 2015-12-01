FROM python:2.7

MAINTAINER Aldo Culquicondor "aldo@amigocloud.com"

LABEL description="Flower for AmigoProxy"

RUN pip install flower==0.8.3

ADD ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["flower"]

EXPOSE 5555
