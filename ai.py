from __future__ import print_function
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import time
import speech_recognition as sr
import pyttsx3 as p
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pytz
import subprocess
import wolframalpha


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
DAYS = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
MONTHS = ['january','february','march','april','may','june','july','august','september','october','november','december']
DAY_EXTENSIONS = ['rd','th','sd','nd']


def speak(text):
    engine = p.init()
    engine.say(text)
    engine.runAndWait()



def get_audio():
    r = sr.Recognizer()
    with sr.Microphone as source:
        audio = r.listen(source)
        said = ('')
        try:
            said = r.recognize_google(audio)
        except Exception as e:
            print("Exception" + str(e))
    return said.lower()


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service


def get_events():
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)


    events_result = service.events().list(calendarId='primary', timeMin= date.isoformat() , timeMax = end_date.isoformat(),singleEvents=True,orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak('No upcoming events found.')
    else:
        speak(f'You have {len(events)} on this day')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split("T"[1]).split('-')[0])
            if int(start_time.split(':')[0]) < 12:
                start_time = start_time + 'pm'
            else:
                start_time = str(int(start_time.split(':')[0])-12) + start_time.split(':')[1]
                start_time = start_time + 'am'

            speak(event["summary"] + 'at' + start_time)

def get_date(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count(today) > 0:
        return today

    day = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(day)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENSIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass

    if month < today.month and month != -1:
        year = year +1

    if day < today.day and month != -1 and day != -1:
        month = month + 1

    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif == -1:
            dif += 7
            if text.count('next') >= 1:
                dif += 7

        return today + datetime.timedelta(dif)
    if month == -1 or day == -1:
        return none

    return datetime.date(month=month,year=year,day=day)


def note(text):
    date = datetime.datetime.now()
    filename = str(date).replace('-',':') + 'note.txt'
    with open(filename,'w') as f:
        f.write(text)

    subprocess.Popen(['note pad.exe' , filename])


wake = 'Hey Chanch'
service = authenticate_google()


while True:
    print('Listening...')
    text = get_audio()
    
    if text.count(wake) > 0:
        speak('I am ready')
        text = get_audio()

    try:
        app_id = ' 7J8JK2-5YPTPW7KTH'
        client = wolframalpha.Client(app_id)
        res = client.query(text)
        answer = next(res.results).text
        speak(answer)
    
    except:
            wikipedia.summary(text)
            speak(answer)

        if:
            for phrase in CALENDAR_STR:

                if phrase in text:
                    date = get_date(text)
                if date:
                    get_events(date,service)
                else:
                    speak("I don't understand")


            for phrase in NOTE_STR:
                
                if phrase in text:
                    speak('what note should i write')
                    note_text = get_audio()
                    note(note_text)
                    speak("I've made a note of that")



































































































































































































































































































































































































































































            


