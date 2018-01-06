#!/usr/bin/env python
import sys
from datetime import datetime
from dateutil import parser
import gcal
import fitbit_api
from cal_event import CalendarEvent

def register_fitbit_to_gcal(fitbit_cred, gcal_sleep_cal_id, gcal_activity_cal_id, data_day = datetime.today(), time_zone="Asia/Tokyo"):
    # 1. get auth of fitbit api
    authd_client, err = fitbit_api.auth_fitbit(fitbit_cred)
    if authd_client == None:
        sys.exit("authd_client is None : {}".format(err))

    # 2. send request to fitbit
    sleep_data_list = fitbit_api.get_sleeps(authd_client, data_day)
    if sleep_data_list == None:
        sys.exit("could not get sleep data")
    if len(sleep_data_list) == 0:
        print("No sleep on this day")
    sleep_events = []
    # sometime you sleep multitimes...
    for sleep_data in sleep_data_list:
        sleep_event = sleep2event(sleep_data)
        sleep_events.append(sleep_event)

    activity_data_list = fitbit_api.get_activities_of_date(authd_client, data_day)
    if activity_data_list == None:
        sys.exit("could not get activity data")
    if len(activity_data_list) == 0:
        print("No activity on this day")
    activity_events = []
    for activity_data in activity_data_list:
        activity_event = activity2event(activity_data)
        activity_events.append(activity_event)

    # 3. send fitbit data to google calendar
    gcal_cred = gcal.get_credentials()
    auth_http, err = gcal.authorize_http(gcal_cred)
    if err != None:
        print("authorization for google cal is failed: ", err)
        sys.exit(1)

    for sleep_event in sleep_events:
        gcal.create_event(auth_http, sleep_event.title,
            sleep_event.start_datetime, sleep_event.end_datetime,
            description=sleep_event.description,
            calendar_id=gcal_sleep_cal_id,
            time_zone=time_zone)

    for activity_event in activity_events:
        gcal.create_event(auth_http, activity_event.title,
            activity_event.start_datetime, activity_event.end_datetime,
            description=activity_event.description,
            calendar_id=gcal_activity_cal_id,
            time_zone=time_zone)


def sleep2event(sleep_data):
    '''
    Convert sleep data for making calendar event
    '''
    minutes_asleep = int(sleep_data["minutesAsleep"])
    sleep_hour = minutes_asleep / 60
    sleep_min = minutes_asleep % 60
    actual_sleep_str = "{:02d}:{:02d}".format(sleep_hour, sleep_min)
    # event title
    title = "Sleep " + actual_sleep_str
    # event description
    description = \
    "Date Of Sleep  : {}\n" \
    "Actual Sleep   : {}\n" \
    "Minutes Awake  : {}min\n" \
    "Efficiency     : {}%\n".format(sleep_data["dateOfSleep"], actual_sleep_str, sleep_data["minutesAwake"], sleep_data["efficiency"])

    # event start stop
    start_datetime = datetime.strptime(sleep_data["startTime"], "%Y-%m-%dT%H:%M:%S.%f") # 2017-12-29T02:28:30.000
    end_datetime = datetime.strptime(sleep_data["endTime"], "%Y-%m-%dT%H:%M:%S.%f") # 2017-12-29T08:28:30.000

    event = CalendarEvent(title, description, start_datetime, end_datetime)
    return event

def activity2event(activity_data):
    '''
    Convert activity data for making calendar event
    '''
    # ignore ms and convert it to seconds
    duration = int(activity_data["duration"]) / 1000
    duration_hour = duration / 3600
    duration_min = (duration % 3600) / 60
    duration_sec = duration % 60

    activity_name = activity_data["activityName"]
    title = "{} - {}h {}m {}s".format(activity_name, duration_hour, duration_min, duration_sec)
    description = \
    "Average Heart Rate : {} beats/min\n" \
    "Calories           : {} cal\n" \
    "Steps              : {}\n".format(activity_data["averageHeartRate"], activity_data["calories"], activity_data["steps"])

    # event start stop
    start_datetime = parser.parse(activity_data["startTime"]) # 2017-12-29T02:28:30.000+09:00
    event = CalendarEvent(title, description, start_datetime, duration=duration)
    return event

def activity_summary2event(activity_data):
    '''
    TODO: Need further imprementation
    Convert activity summary data for making calendar event
    '''
    title = "Activity " + activity_data["name"]
    duration = activity_data["duration"]
    description = \
    "Calories    : {} cal\n" \
    "Description : {}\n" \
    "Distance    : {}\n" \
    "Duration    : {}\n".format(activity_data["calories"], activity_data["description"], activity_data["distance"], )

    # event start stop
    start_date = datetime.strptime(activity_data["startDate"], "%Y-%m-%d") # 2017-12-28
    # TODO: has to calcurate end_time from start_time and duration
    #start_time = datetime.strptime(activity_data["startTime"], "%H:%M") # 2017-12-29T02:28:30.000
    #start_datetime=
    #end_datetime = datetime.strptime(activity_data["endTime"], "%Y-%m-%dT%H:%M:%S.%f") # 2017-12-29T08:28:30.000
    #return title, description, start_datetime, end_datetime
