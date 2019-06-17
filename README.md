# FlaskMock

### Start mock server

`FLASK_APP=flaskmock.py flask run`

### Configuration

API JSON schemas, validators and request processors should be placed under respective API path.

Example: `./api/task/sample-endpoint/`

See included example for detailed info and naming conventions.

### JSON schema files

Online schema generator: https://jsonschema.net/

### Docker

Build image: `docker build --rm -t flaskmock:latest .`

Start interactively: `docker run --rm -p 5000:5000 -it flaskmock`

Start detached: `docker run --rm -p 5000:5000 -d flaskmock`