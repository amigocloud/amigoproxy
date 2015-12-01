FROM python:2.7

MAINTAINER Aldo Culquicondor "aldo@amigocloud.com"

LABEL description="Celery for AmigoProxy"

ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt

ADD ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["celery"]
ENV C_FORCE_ROOT=1
