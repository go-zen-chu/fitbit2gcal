#!/usr/bin/env python
import os
from fitbit2gcal import fitbit2gcal, fitbit_cred
from datetime import datetime, timedelta

if __name__ == '__main__':
    fb_client = os.getenv("FITBIT2CAL_FB_CLIENT")
    fb_secret = os.getenv("FITBIT2CAL_FB_SECRET")
    fb_access_token = os.getenv("FITBIT2CAL_FB_ACCESS_TOKEN")
    fb_refresh_token = os.getenv("FITBIT2CAL_FB_REFRESH_TOKEN")

    fb_cred = fitbit_cred.FitbitCred(fb_client, fb_secret, fb_access_token, fb_refresh_token)

    gcal_sleep_cal_id = os.getenv("FITBIT2CAL_GCAL_SLEEP_ID")
    gcal_activity_cal_id = os.getenv("FITBIT2CAL_GCAL_ACTIVITY_ID")

    time_zone = os.getenv("FITBIT2CAL_TIME_ZONE")
    yesterday = datetime.today() - timedelta(days=1)
    fitbit2gcal.register_fitbit_to_gcal(fb_cred, gcal_sleep_cal_id, gcal_activity_cal_id, data_day=yesterday, time_zone=time_zone)
