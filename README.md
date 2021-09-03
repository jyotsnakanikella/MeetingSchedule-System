# MeetingSchedule-System

The below mentioned usecases need to be handled using python, Postgresql, Flask:

1. User should be able to add an event which occurs on a fixed date and time
  a. Ex. User adds an event for 17th April 2021 16:00 – 19:00
2. User should be able to add a recurring event
  a. Recurrence can be any combination of two days of the week. For ex. Mon, Thu or Sat, 
    Sun etc.
  b. Event should have a start date
  c. Event could be continued indefinitely (end date may not be supplied by the user)
  d. Ex. User adds a recurring event from 17th April 12:00 – 13:00 which occurs definitely 
    on every Mon, Sat
3. User should be able to alter one instance of an already existing recurring event
  a. User may change the time of that specific instance
  b. User may change the date of that specific instance
  c. Ex. User changes the time 20th April instance of the recurring event added in step 2 to 
    from 12:00 – 13:00 to 16:00 - 16:45
4. User should be able to alter an already existing recurring event from one instance onwards
  a. User may change the time of all the upcoming instance from the selected instance
  b. User may change the date of all the upcoming instance from the selected instance
  c. Ex. User changes the time from the 20th April instance of the recurring event added in 
    step 2 to from 12:00 – 13:00 to 16:00 - 16:45
5. User should be able to fetch the calendar for the given date range, start date and end date 
both inclusive
  a. Ex. User fetches the calendar between 17th April 2021 – 19th June 2022
 
 
Important restriction(s):
• User can never have any two instances of an event overlapping. For ex, an event of 15th April 
2021 16:00 – 17:00 cannot co-exist with 15th April 16:45-17:15
  
