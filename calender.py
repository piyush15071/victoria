# Functions : get_credentials, add_event, returnMonth, playDate, main

# Needs authentication when runs first time
# authentication through default browser and oAuth

from __future__ import print_function
import indepFunc as ip
import httplib2
import os

from termcolor import colored
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
import time

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.
    
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    
    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print (colored("\nStoring credentials to " + credential_path + "\n",'red'))
    return credentials

def add_event(service):
    event = {
      'summary': 'Google I/O 2015',
      'location': '800 Howard St., San Francisco, CA 94103',
      'description': 'A chance to hear more about Google\'s developer products.',
      'start': {
        'dateTime': '2017-05-28T09:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
        },
      'end': {
        'dateTime': '2017-05-28T17:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
        },
      'reminders': {
        'useDefault': True,
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print (colored('\nEvent created: %s\n' % (event.get('htmlLink')),'green'))

# returns month's name according to corresponding number
def returnMonth(i):
    if(i=="01"): return "January"
    elif(i=="02"): return "February"
    elif(i=="03"): return "March"
    elif(i=="04"): return "April"
    elif(i=="05"): return "May"
    elif(i=="06"): return "June"
    elif(i=="07"): return "July"
    elif(i=="08"): return "August"
    elif(i=="09"): return "September"
    elif(i=="10"): return "October"
    elif(i=="11"): return "November"
    elif(i=="12"): return "December"

def playDate(s):
    # if time is present in event
    if(len(s)>10):
        # play month
        d = list(s[0:10].split("-"))
        play = d[2]+"th "+returnMonth(d[1])
        ip.play(play)

        # play time
        time = s[11:16]
        play = time+" hours"
        ip.play(play)
    # if only date is present
    else:
        d = list(s.split("-"))
        play = d[2]+"th "+returnMonth(d[1])
        ip.play(play)

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # print (colored('\nGetting the upcoming 10 events\n','green'))
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=5, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    # if there are no upcoming events
    if not events:
        print (colored('\nNo upcoming events found.\n','red'))
    for event in events:
        # loop through events
        start = event['start'].get('dateTime', event['start'].get('date'))
        dateTime = event['start'].get('dateTime')
        if(dateTime==None):
            dateTime = event['start'].get('date')
        eventName = event['summary']
        print (colored("\n"+dateTime+" :-: "+eventName+"\n",'green'))
        ip.play(eventName)
        playDate(dateTime)
        # two seconds delay between playing every event
        time.sleep(2)

    # lines for adding an event (future scope)
    # print("add event enter")
    # add_event(service)
    # print("add event exit")


if __name__ == '__main__':
    main()