FROM python:2.7

MAINTAINER Aldo Culquicondor "aldo@amigocloud.com"

LABEL description="Gunicorn for AmigoProxy"

ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt

ADD ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["gunicorn", "amigoproxy.wsgi", "--workers", "8", "--bind", "0.0.0.0:9000", "--timeout", "30", "--worker-class", "gevent"]

RUN ln -s /srv/amigoproxy/manage.py /usr/local/bin/manage.py

EXPOSE 9000
