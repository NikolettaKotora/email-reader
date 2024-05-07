import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path
import base64
import email

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

subject=[]
senders=[]
body=[]

def myEmails():
    '''myEmails function will create token and read emails'''
    creds=None

    #Creating token
    if os.path.exists('token.json'):
        creds=Credentials.from_authorized_user_file('token.json', SCOPES)
    elif not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            #creds.refresh(Request())
        else:
            flow= InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds=flow.run_local_server(port=0)
            with open ('token.json', 'w') as token:
                token.write(creds.to_json())




    try:
        #Reading emails
        service= build('gmail', 'v1', credentials=creds)
        result= service.users().messages().list(userId='me').execute()
        messages = result.get('messages')
        for i in messages:
            txt = service.users().messages().get(userId='me',id=i['id']).execute()
            payload = txt['payload']
            headers = payload['headers']
            for i in headers:
                if i['name'] == 'Subject':
                    subject.append(i['value'])
                elif i['name'] == 'From':
                    sender = i['value']
                    senders.append(sender)
            parts= payload.get('parts')[0]
            data=parts['body']['data']
            data=data.replace('-', '+').replace('-', '/')
            decode_data=base64.b64decode(data)
            body.append(decode_data)
            print(body)
    
    except HttpError as error:
        print(f'An error occured: {error}')







myEmails()