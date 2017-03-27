# docker-unoconv-flask

Dockerimage to run unoconv as a webservice using [Flask](https://github.com/pallets/flask) and [Flask-RESTful](https://github.com/flask-restful/flask-restful).

If you prefer a pre-build version it is available from [hub.docker.com](https://hub.docker.com/r/jordanorc/docker-unoconv-flask)
just do a regular pull

```bash
$ docker pull jordanorc/docker-unoconv-flask
```

## Build

```bash
$ docker build -t docker-unoconv-flask .
```

## Run - example
```bash
$ docker run -d -p 5000:5000 --name unoconv docker-unoconv-flask
```

or if you use the pre-build version

```bash
$ docker run -d -p 5000:5000 --name unoconv jordanorc/docker-unoconv-flask
```

## Usage

Post the file you want to convert to the server and get the converted file in return.

API for the webservice is /unoconv/{format-to-convert-to} so a docx to pdf would be

```bash
$ curl --form file=@myfile.docx http://localhost:5000/unoconv/pdf/ > myfile.pdf
```
## License
[MIT](LICENSE)
