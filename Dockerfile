FROM docker:18.09.5-dind AS docker
FROM docker/compose:1.23.2 AS docker-compose
FROM python:3.7.2-stretch

COPY --from=docker-compose /usr/local/bin/docker-compose /usr/local/bin/docker-compose
COPY --from=docker /usr/local/bin/docker /usr/local/bin/docker

RUN pip install "Flask==1.0.2" \
 && mkdir /srv/api/

COPY api /srv/api/
WORKDIR /srv/api

ENTRYPOINT ["python"]
CMD ["/srv/api/api.py"]
