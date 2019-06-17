# FlaskMock

### Requirements

Python 2.7+

Linux users: `sudo pip install Flask jsonschema requests objectpath`

MAC users: `pip install --user Flask jsonschema requests objectpath`

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

### Performing callbacks/postbacks

What is callback/postback? It's an async call to your app to confirm that some kind of time-consuming task your app was waiting for was eventually performed.

Example: your customer submitted all CC data and we stored this TXn as pending confirmation. The only thing we need is a postback with SMS confirmation code (actually a token from acquirer).

It can be performed from route definition (in that case it will be fired ignoring any validation errors), or via processor extension (will be called only if previous validations went okay).

In fact, it's just a function submitted to the thread pool scheduled to run as soon as it possible.

Payload, callback function logic - it's up to you.

This enables us to build almost identical-to-prod mocks.

Due to the limitations of the Flask/WSGI we cannot utilize post_response actions (this will need tight integration with the WSGI server), so the only option is to introduce a reasonable sleep into the callback function.