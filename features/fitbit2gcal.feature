Feature: Convert Fitbit Data to Event
  Scenario: run sleep2event
     Given initial state
      when valid sleep data are passed
      then sleep data are converted to event

  Scenario: run activity2event
     Given initial state
      when valid activity data are passed
      then activity data are converted to event
