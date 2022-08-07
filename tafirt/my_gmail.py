from __future__ import print_function
from itertools import count

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import base64
import email
from datetime import datetime
import time
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
def get_lables(service, user_id):
    return  service.users().labels().list(userId=user_id).execute()

def get_messages(service, user_id,my_query):
  try:
    return service.users().messages().list(userId=user_id,q=my_query).execute()
  except Exception as error:
    print('An error occurred: %s' % error)

def get_message(service, user_id, msg_id):
  try:
    return service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
  except Exception as error:
    print('An error occurred: %s' % error)

def get_mime_message(service, user_id, msg_id):
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id,
                                             format='raw').execute()
    #print('Message snippet: %s' % message['snippet'])
    msg_str = base64.urlsafe_b64decode(message['raw'].encode("utf-8")).decode("utf-8")
    mime_msg = email.message_from_string(msg_str)

    return mime_msg
  except Exception as error:
    print('An error occurred: %s' % error)
def get_attachments(service, user_id, msg_id, store_dir):
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()

    for part in message['payload']['parts']:
      if(part['filename'] and part['body'] and part['body']['attachmentId']):
        attachment = service.users().messages().attachments().get(id=part['body']['attachmentId'], userId=user_id, messageId=msg_id).execute()

        file_data = base64.urlsafe_b64decode(attachment['data'].encode('utf-8'))
        path = ''.join([store_dir, part['filename']])

        f = open(path, 'wb')
        f.write(file_data)
        f.close()
        return True,path
    return False,None
  except Exception as error:
    print('An error occurred: %s' % error)
    return False,None
  
def get_last_month():
    now = datetime.now()
    last_month = now.month-1 if now.month > 1 else 12
    query = 'after:{}-0{}-01'.format(now.year,last_month)
    return query

def get_my_email_attachment_by_title(subject,query= get_last_month()): 
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        msgs = get_messages(service,'me',query)
        if msgs['resultSizeEstimate'] ==0:
            return None
        for msgid in msgs['messages']:
                msg = get_mime_message(service,'me',msgid['id'])
                msg_subject = msg['Subject']
                print(msg_subject)
                if  msg_subject == subject:
                    return get_attachments(service,'me',msgid['id'],'./')
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')
        

def get_my_email_last_attachment(query=get_last_month()):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        msgs = get_messages(service,'me',query)
        if msgs['resultSizeEstimate'] ==0:
            return None
        for msgid in msgs['messages']:
                    is_have_attachments,path = get_attachments(service,'me',msgid['id'],'./')
                    if is_have_attachments:
                        return is_have_attachments,path
        return False,None
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')
        return False,None
  
def main():
    query = 'after:2022-08-05'
    get_my_email_last_attachment(query)

if __name__ == '__main__':
    main()