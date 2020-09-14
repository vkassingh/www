import sys
import pysher
import time
import json

import pickle
import os.path
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Add a logging handler so we can see the raw communication data
import logging
root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
root.addHandler(ch)

pusher = pysher.Pusher('SECRET', cluster='eu')
service = None


def message_handler(message_data):
    global service
    message = json.loads(message_data)
    if message['body'].strip().startswith('Q:'):
        question = message['body'].strip()[2:].strip()
        print(f"Found question: {message['user']['name']} > {question}")
        values = [[
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
            message['user']['name'],
            question,
        ]]
        body = {
            'values': values
        }
        service.spreadsheets().values().append(
            spreadsheetId=DOCUMENT_ID, range='Sheet1',
            valueInputOption='USER_ENTERED', body=body).execute()


def connect_handler(data):
    channel = pusher.subscribe('hopin-chat-stage-SECRET')
    channel.bind('message', message_handler)


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID of a sample document.
DOCUMENT_ID = 'SECRET'


def main():
    global service
    pusher.connection.bind('pusher:connection_established', connect_handler)
    pusher.connect()

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

    service = build('sheets', 'v4', credentials=creds)

    while True:
        # Do other things in the meantime here...
        time.sleep(1)


if __name__ == '__main__':
    main()
