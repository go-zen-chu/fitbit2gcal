#!/usr/bin/env python
from fitbit2gcal import fitbit_api
from flask import Flask
import logging

# rest api
app = Flask(__name__)

def refresh_fitbit_token():

    authd_client =
    # refresh token via fitbit api
    token =
    # store to environment variable



@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

@app.route('/refresh')
# This function should be called every 6 hours to maintain fitbit access
def route_refresh_fitbit_token():
    '''
    Refresh Fitbit token
    '''

    refresh_fitbit_token()
    return 'Hello World!'

@app.route('/fitbit2gcal')
def route_send_fb_events2gcal():
    send_fb_events2gcal()
    return 'Hello World!'

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    
    app.run(host='127.0.0.1', port=8080, debug=True)
