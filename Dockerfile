FROM python:alpine

ENV LC_ALL=en_US.UTF-8 \
	LANG=en_US.UTF-8 \
	LANGUAGE=en_US.UTF-8 \
	UNO_URL=https://raw.githubusercontent.com/dagwieers/unoconv/master/unoconv

# copy salus files
COPY . /unoconv

RUN apk add --no-cache \
        curl \
        libreoffice-common \
        libreoffice-writer \
        ttf-droid-nonlatin \
        ttf-droid \
        ttf-dejavu \
        ttf-freefont \
        ttf-liberation \
    && rm -rf /unoconv/.git \
    && curl -Ls $UNO_URL -o /bin/unoconv \
    && chmod +x /bin/unoconv \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && cd /unoconv \
    && pip install -r requirements.txt \
    && apk del curl \
    && rm -rf /var/cache/apk/*

WORKDIR /unoconv

EXPOSE 5000

ENTRYPOINT python3 /unoconv/app.py && /bin/unoconv --listener --server=0.0.0.0 --port=2002
