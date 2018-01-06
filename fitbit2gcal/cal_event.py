#!/usr/bin/env python
from datetime import datetime, timedelta

class CalendarEvent:
    def __init__(self, title, description, start_datetime, end_datetime = None, duration=-1):
        '''
        @params duration : in seconds
        '''
        self.title = title
        self.description = description
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        if duration >= 0:
            self.end_datetime = self.start_datetime + timedelta(seconds=duration)
