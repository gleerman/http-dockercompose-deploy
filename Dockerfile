FROM frolvlad/alpine-glibc

RUN apk add docker \
    && apk add --no-cache python3 \
    && python3 -m ensurepip \
    && rm -r /usr/lib/python*/ensurepip \
    && pip3 install --upgrade pip setuptools \
    && if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi \
    && if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi \
    && rm -r /root/.cache \
    && pip3 install "Flask==1.0.2" \
    && pip3 install 'docker-compose==1.20.1' \
    && mkdir /srv/api/

COPY api /srv/api/
WORKDIR /srv/api

ENTRYPOINT ["python"]
CMD ["/srv/api/api.py"]
