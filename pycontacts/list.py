"""
This was based on:
- https://developers.google.com/people/quickstart/python
"""

import argparse
import os
import os.path
import os.path

import apiclient
import httplib2
import oauth2client
import oauth2client.tools
import oauth2client.file
import oauth2client.client

# https://developers.google.com/people/api/rest/v1/people/get
APPLICATION_NAME = 'pycontacts'
SCOPES = 'https://www.googleapis.com/auth/contacts.readonly'
CLIENT_SECRET_FILE = os.path.expanduser('~/.client_secrets/{}.json'.format(APPLICATION_NAME))
flags = argparse.ArgumentParser(parents=[oauth2client.tools.argparser]).parse_args()


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
    credential_path = os.path.join(credential_dir, '{}.json'.format(APPLICATION_NAME))

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = oauth2client.client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = oauth2client.tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build(
        'people',
        'v1',
        http=http,
        discoveryServiceUrl='https://people.googleapis.com/$discovery/rest',
    )

    people = service.people()
    # print(dir(people))
    # connections = people.connections()
    results = people.connections().list(
        resourceName='people/me',
        personFields="names",
        pageSize=2000,  # 2000 is the maximum
    ).execute()
    # debug
    # print(results.keys())
    connections = results.get('connections')

    display_names = []
    for person in connections:
        # print(person)
        # debug
        # print(person.keys())
        # rn=person['resourceName']
        names = person['names']
        name = names[0].get('displayName')
        display_names.append(name)

    display_names.sort()
    for x in display_names:
        print(x)


if __name__ == '__main__':
    main()
