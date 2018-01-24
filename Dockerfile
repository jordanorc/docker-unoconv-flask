FROM python:3.6.4-alpine3.6

ENV LC_ALL=en_US.UTF-8 \
	LANG=en_US.UTF-8 \
	LANGUAGE=en_US.UTF-8 \
	UNO_URL=https://raw.githubusercontent.com/dagwieers/unoconv/master/unoconv

# copy unconv files
COPY ./requirements.txt /tmp/requirements.txt

RUN apk add --no-cache \
        --virtual .build-deps \
        gcc \
        g++ \
        linux-headers \
        libc-dev \
    && apk add --no-cache \
        curl \
        libreoffice-common \
        libreoffice-writer \
        libreoffice-calc \
        libreoffice-impress \
        ttf-droid-nonlatin \
        ttf-droid \
        ttf-dejavu \
        ttf-freefont \
        ttf-liberation \
    && curl -Ls $UNO_URL -o /bin/unoconv \
    && chmod +x /bin/unoconv \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && pip install -r /tmp/requirements.txt \
    && apk del curl \
    && rm -rf /var/cache/apk/* \
    && rm -rf /root/.cache/ \
    && rm -rf /tmp/requirements.txt \
    && apk del .build-deps

# copy unconv files
COPY . /unoconv

RUN rm -rf /unoconv/.git

WORKDIR /unoconv

EXPOSE 5000

ENTRYPOINT circusd circus.ini
