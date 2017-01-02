#!/usr/bin/python3

import os.path
import httplib2
import os
import os.path
import argparse
import oauth2client
import apiclient

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/people.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/contacts.readonly'
CLIENT_SECRET_FILE = os.path.expanduser('~/.myworld/client_id.json')
APPLICATION_NAME = 'People API Python Quickstart'


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
                                   'people.googleapis.com-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = oauth2client.client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = oauth2client.tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = oauth2client.tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google People API.

    Creates a Google People API service object and outputs the name if
    available of 10 connections.
    """
    flags = argparse.ArgumentParser(parents=[oauth2client.tools.argparser]).parse_args()
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('people', 'v1', http=http,
        discoveryServiceUrl='https://people.googleapis.com/$discovery/rest')

    print('List 10 connection names')
    results = service.people().connections().list(
        resourceName='people/me',
        pageSize=500,
    ).execute()
    # debug
    #print(results.keys())
    connections = results.get('connections')

    l=[]
    for person in connections:
        print(person)
        # debug
        #print(person.keys())
        #rn=person['resourceName']
        names = person['names']
        name = names[0].get('displayName')
        l.append(name)
    
    l.sort()
    for x in l:
        print(x)


if __name__ == '__main__':
    main()
