from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import date

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def auth():
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

    return build('gmail', 'v1', credentials=creds)

def get_label(service):

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        padding = str(len(str(len(labels))))
        options = ['[' + ("{0:0>"+padding+"}").format(i) + '] ' + label['name'] for i,label in enumerate(labels)]
        for option in options:
            print(option)
        
        selection = -1
        while selection not in range(0,len(options)):
            selection = int(input())
        return labels[selection]

def get_emails(service, label):
    results = service.users().messages().list(
        userId='me',
        labelIds=[label['id']],
        q="after:" + str(date.today())
    ).execute()
    messages = results.get('messages', [])
    if len(messages) == 0:
        print('No new mail today.')
    else:

        for message in messages:
            email = service.users().messages().get(
                userId='me',
                id=message['id'],
                format='full'
            ).execute()
            print('Subject: "'+list(filter(lambda header: header['name'] == 'Subject', email['payload']['headers']))[0]['value']+'"')
    

if __name__ == '__main__':
    service = auth()
    label = get_label(service)
    emails = get_emails(service, label)
