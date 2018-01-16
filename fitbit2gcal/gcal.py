#!/usr/bin/env python
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar' # read write
CLIENT_SECRET_FILE = 'gcal_client_secret.json'
CRED_STORE_FILE = 'gcal_cred_store.json'
APPLICATION_NAME = 'fitbit2gcal'

def get_package_root():
    return os.path.dirname(os.path.abspath(__file__))

def get_pj_root():
    return os.path.dirname(get_package_root())

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    cred_store_path = os.path.join(get_pj_root(), CRED_STORE_FILE)
    store = Storage(cred_store_path)
    credentials = store.get()
    # check credential valid
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ', cred_store_path)
    return credentials

def authorize_http(credentials):
    if credentials == None:
        return None, Exception("credential is none")
    return credentials.authorize(httplib2.Http()), None

def create_event(auth_http, title, start_datetime, end_datetime, description='', location='', calendar_id='primary', time_zone='UTC'):
    """
    create event in google calendar
    """
    service = discovery.build('calendar', 'v3', http=auth_http)

    event = {
      'summary': title,
      'location': location,
      'description': description,
      'start': {
        'dateTime': start_datetime.strftime("%Y-%m-%dT%H:%M:%S"), #'2018-01-01T09:00:00+09:00',
        'timeZone': time_zone,
      },
      'end': {
        'dateTime': end_datetime.strftime("%Y-%m-%dT%H:%M:%S"), #'2018-01-01T17:00:00+09:00',
        'timeZone': time_zone,
      },
    }
    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    return None
