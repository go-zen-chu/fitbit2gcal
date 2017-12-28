#!/usr/bin/env python
import sys
from datetime import datetime
from fitbit_api import FitbitAPI
import gcal

def register_fitbit_to_gcal(client_id, client_secret, access_token, refresh_token, data_day = datetime.today()):
    # 1. get request
    # 2. manage tokens
    fb = FitbitAPI()
    authd_client, err = fb.auth_fitbit(client_id, client_secret, access_token, refresh_token)
    if authd_client == None:
        print("authd_client is None : ", err)
        sys.exit(1)
    # 3. send request to fitbit
    sleep_data = fb.get_sleeps(authd_client, data_day)
    if sleep_data == None:
        print("could not get data")
        sys.exit(1)
    print(sleep_data)
    # 4. if data is retreived

    # 5. convert to google calendar event
    # 6. get google api tokens
    gcal.create_event("vu5v3v9mcvmm0fppe79lo6jf7c@group.calendar.google.com")
    # 7. send to google calendar
