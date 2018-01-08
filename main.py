#!/usr/bin/env python
import os
from fitbit2gcal import fitbit2gcal, fitbit_cred
from datetime import datetime, timedelta
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sending Fitbit data to Google Calendar')

    # fitbit
    parser.add_argument('--fb-client', type=str, required=True, default=os.getenv("FITBIT2CAL_FB_CLIENT", help='Fitbit API oauth2 client')
    parser.add_argument('--fb-secret', type=str, required=True, default=os.getenv("FITBIT2CAL_FB_SECRET", help='Fitbit API oauth2 secret')
    parser.add_argument('--fb-access-token', type=str, required=True, default=os.getenv("FITBIT2CAL_FB_ACCESS_TOKEN", help='Fitbit API oauth2 access token')
    parser.add_argument('--fb-refresh-token', type=str, required=True, default=os.getenv("FITBIT2CAL_FB_REFRESH_TOKEN", help='Fitbit API oauth2 refresh token')
    # google calendar
    parser.add_argument('--gcal-sleep-id', type=str, required=True, default=os.getenv("FITBIT2CAL_GCAL_SLEEP_ID", help='Google Calendar storing sleep event')
    parser.add_argument('--gcal-activity-id', type=str, required=True, default=os.getenv("FITBIT2CAL_GCAL_ACTIVITY_ID", help='Google Calendar storing activity event')

    parser.add_argument('--gcal-sleep-id', type=str, metavar='plane_txt_file', help='Encrypt specified file to .enc file. This function does not record your password. Do not forget it.')
    parser.add_argument('-d',  type=str, metavar='enc_file', help='Decrypt .enc file with password')
    fb_client = os.getenv("FITBIT2CAL_FB_CLIENT")
    fb_secret = os.getenv("FITBIT2CAL_FB_SECRET")
    fb_access_token = os.getenv("FITBIT2CAL_FB_ACCESS_TOKEN")
    fb_refresh_token = os.getenv("FITBIT2CAL_FB_REFRESH_TOKEN")

    fb_cred = fitbit_cred.FitbitCred(fb_client, fb_secret, fb_access_token, fb_refresh_token)

    gcal_sleep_cal_id = os.getenv("FITBIT2CAL_GCAL_SLEEP_ID")
    gcal_activity_cal_id = os.getenv("FITBIT2CAL_GCAL_ACTIVITY_ID")

    time_zone = os.getenv("FITBIT2CAL_TIME_ZONE")
    yesterday = datetime.today() - timedelta(days=1)
    fitbit2gcal.send_fb_events2gcal(fb_cred, gcal_sleep_cal_id, gcal_activity_cal_id, data_day=yesterday, time_zone=time_zone)
