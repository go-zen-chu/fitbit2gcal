#!/usr/bin/env python
from behave import *
import os
from datetime import datetime, timedelta

from fitbit2gcal import fitbit_cred
from fitbit2gcal import fitbit_api

"""
This file defines common functions that are used in steps.
"""

@given('initial state')
def step_impl(context):
    """
    Do nothing because it is just an initial state
    """
    pass

@when('datetime is passed')
def step_impl(context):
    dt = datetime(2017, 12, 28)
    context.datetime = dt
    assert dt != None

@when('yesterday datetime is passed')
def step_impl(context):
    dt = datetime.today() - timedelta(days=1)
    context.datetime = dt
    assert dt != None

@when('3day before datetime is passed')
def step_impl(context):
    dt = datetime.today() - timedelta(days=3)
    context.datetime = dt
    assert dt != None

def get_fb_cred():
    fb_client = os.getenv("FITBIT2CAL_FB_CLIENT")
    fb_secret = os.getenv("FITBIT2CAL_FB_SECRET")
    fb_access_token = os.getenv("FITBIT2CAL_FB_ACCESS_TOKEN")
    fb_refresh_token = os.getenv("FITBIT2CAL_FB_REFRESH_TOKEN")

    fb_cred = fitbit_cred.FitbitCred(fb_client, fb_secret, fb_access_token, fb_refresh_token)
    return fb_cred

def get_authd_client():
    #TODO: I know it has to be mocked...
    #TODO: I am planning to use unittest.mock
    fb_cred = get_fb_cred()
    authd_client, err = fitbit_api.auth_fitbit(fb_cred)
    assert err == None
    return authd_client
