#!/usr/bin/env python
from behave import *
import step_common
from fitbit2gcal import fitbit_api

@when('credential is passed')
def step_impl(context):
    context.authd_client = step_common.get_authd_client()

@then('return authenticated client')
def step_impl(context):
    assert context.authd_client != None

@given('having authenticated client')
def step_impl(context):
    context.authd_client = step_common.get_authd_client()
    assert context.authd_client != None

@then('return sleep data')
def step_impl(context):
    sleep_data = fitbit_api.get_sleeps(context.authd_client, context.datetime)
    assert sleep_data != None

@then('return activity summary data')
def step_impl(context):
    activity_data = fitbit_api.get_activity_summary(context.authd_client, context.datetime)
    assert activity_data != None
    assert context.failed == False

@then('return activity data after specified date')
def step_impl(context):
    activity_data = fitbit_api.get_activities_after(context.authd_client, context.datetime)
    assert activity_data == None
    assert context.failed == False

@then('return activity data')
def step_impl(context):
    activity_data = fitbit_api.get_activity_summary(context.authd_client, context.datetime)
    print(activity_data)
    assert activity_data == None
    assert context.failed == False
