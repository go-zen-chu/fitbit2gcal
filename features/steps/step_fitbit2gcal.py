#!/usr/bin/env python
from behave import *
import step_test_data
from fitbit2gcal import fitbit2gcal

@when('valid sleep data are passed')
def step_impl(context):
    context.sleep_data = step_test_data.valid_sleep_data['sleep'][0]
    assert context.sleep_data != None

@then('sleep data are converted to event')
def step_impl(context):
    event = fitbit2gcal.sleep2event(context.sleep_data)
    assert event.title == "Sleep 5:29"
    assert context.failed == False

@when('valid activity data are passed')
def step_impl(context):
    context.activity_data = step_test_data.valid_activity_data['activities'][0]
    assert context.activity_data != None

@then('activity data are converted to event')
def step_impl(context):
    event = fitbit2gcal.activity2event(context.activity_data)
    assert event.title == "Sport - 1h 53m 29s"
    assert context.failed == False
