Feature: Handling Google Calendar
  Scenario: get google calendar creds
     Given initial state
      when valid credentials are passed
      then check credentials are not empty

  Scenario: get google calendar authorized http client
     Given valid google calendar credentials
      when authorizing http client
      then check authorized http client is not empty
