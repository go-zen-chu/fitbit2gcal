#!/usr/bin/env python
import os
from fitbit2gcal import fitbit_api, fitbit2gcal, fitbit_cred
from flask import Flask, request
import logging
from datetime import datetime, timedelta
from dateutil import parser as dt_parser

# rest api
app = Flask(__name__)

@app.route('/')
def hello():
    """
    Return a friendly HTTP greeting.
    """
    return 'Hello World!'

def refresh_fitbit_token():
    fb_client = os.getenv("FITBIT2CAL_FB_CLIENT")
    fb_secret = os.getenv("FITBIT2CAL_FB_SECRET")
    fb_access_token = os.getenv("FITBIT2CAL_FB_ACCESS_TOKEN")
    fb_refresh_token = os.getenv("FITBIT2CAL_FB_REFRESH_TOKEN")
    fb_expires_at = os.getenv("FITBIT2CAL_FB_EXPIRES_AT")
    print(type(fb_expires_at))

    fb_cred = fitbit_cred.FitbitCred(fb_client, fb_secret, fb_access_token, fb_refresh_token, fb_expires_at)

    authd_client, err = fitbit_api.auth_fitbit(fb_cred)
    if err != None:
        return err
    # refresh token via fitbit api
    token = authd_client.client.refresh_token()
    print(token)
    # store to environment variable
    return None

@app.route('/refresh')
# This function should be called every 6 hours to maintain fitbit access
def route_refresh_fitbit_token():
    '''
    Refresh Fitbit token
    '''
    err = refresh_fitbit_token()
    if err != None:
        return 'An internal error occurred: <pre>{}</pre>See logs for full stacktrace.'.format(err), 500
    return 'Token Refreshed Successfully'

@app.route('/fitbit2gcal')
def route_send_fb_events2gcal():
    fb_client = os.getenv("FITBIT2CAL_FB_CLIENT")
    fb_secret = os.getenv("FITBIT2CAL_FB_SECRET")
    fb_access_token = os.getenv("FITBIT2CAL_FB_ACCESS_TOKEN")
    fb_refresh_token = os.getenv("FITBIT2CAL_FB_REFRESH_TOKEN")
    fb_expires_at = os.getenv("FITBIT2CAL_FB_EXPIRES_AT")

    if any([fb_client == None, fb_secret == None]):
        return ('Credentials could not be empty.', 400)
    fb_cred = fitbit_cred.FitbitCred(fb_client, fb_secret, fb_access_token, fb_refresh_token, fb_expires_at)

    gcal_sleep_id = os.getenv("FITBIT2CAL_GCAL_SLEEP_ID")
    gcal_activity_id = os.getenv("FITBIT2CAL_GCAL_ACTIVITY_ID")

    yesterday = datetime.today() - timedelta(days=1)
    data_day_str = request.args.get('data_day')
    if data_day_str == None:
        data_day_str = yesterday.strftime('%Y-%m-%d') # set yesterday by default
    data_day = dt_parser.parse(data_day_str)
    print(data_day)

    time_zone = request.args.get('time_zone')
    time_zone = "UTC" if time_zone == None else time_zone

    fitbit2gcal.send_fb_events2gcal(
        fb_cred,
        gcal_sleep_id,
        gcal_activity_id,
        data_day=data_day,
        time_zone=time_zone,
    )
    return 'Fitbit data are registered to google calendar!'

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
