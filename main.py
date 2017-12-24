#!/usr/bin/env python
import os
from fitbit2gcal import fitbit2gcal

if __name__ == '__main__':
    fb_client = os.getenv("FITBIT2CAL_FB_CLIENT")
    fb_secret = os.getenv("FITBIT2CAL_FB_SECRET")
    fb_access_token = os.getenv("FITBIT2CAL_FB_ACCESS_TOKEN")
    fb_refresh_token = os.getenv("FITBIT2CAL_FB_REFRESH_TOKEN")

    fitbit2gcal.register_fitbit_to_gcal(fb_client, fb_secret, fb_access_token, fb_refresh_token)
