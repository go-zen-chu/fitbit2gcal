#!/usr/bin/env python
from behave import *
import step_common
from fitbit2gcal import gcal
from datetime import datetime
@when('valid credentials are passed')
def step_impl(context):
    context.gcal_creds = gcal.get_credentials()

@then('check credentials are not empty')
def step_impl(context):
    assert context.gcal_creds != None
    assert context.failed == False

@given('valid google calendar credentials')
def step_impl(context):
    context.gcal_creds = gcal.get_credentials()
    assert context.gcal_creds != None

@when('authorizing http client')
def step_impl(context):
    context.auth_http, err = gcal.authorize_http(context.gcal_creds)
    assert err == None

@then('check authorized http client is not empty')
def step_impl(context):
    assert context.auth_http != None
    assert context.failed == False
