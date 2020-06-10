"""
The default group of operations that pycontacts has
"""
import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from pytconf.config import register_endpoint, register_function_group

import pycontacts
import pycontacts.version
from pycontacts.configs import ConfigAuthFiles

import gdata.data
import gdata.gauth
import gdata.contacts.client
import gdata.contacts.data

GROUP_NAME_DEFAULT = "default"
GROUP_DESCRIPTION_DEFAULT = "all pycontacts commands"

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/contacts.readonly',
]


def register_group_default():
    """
    register the name and description of this group
    """
    register_function_group(
        function_group_name=GROUP_NAME_DEFAULT,
        function_group_description=GROUP_DESCRIPTION_DEFAULT,
    )


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
)
def version() -> None:
    """
    Print version
    """
    print(pycontacts.version.VERSION_STR)


@register_endpoint(
    configs=[
        ConfigAuthFiles,
    ],
)
def list_contacts():
    credentials = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(ConfigAuthFiles.token):
        with open(ConfigAuthFiles.token, 'rb') as token:
            credentials = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                ConfigAuthFiles.client_secret,
                SCOPES
            )
            credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(ConfigAuthFiles.token, 'wb') as token:
            pickle.dump(credentials, token)
    # print(dir(credentials))
    # print(credentials.token)
    # print(credentials.refresh_token)
    # print(credentials.client_id)
    # print(credentials.client_secret)

    token = gdata.gauth.OAuth2Token(
        client_id=credentials.client_id,
        client_secret=credentials.client_secret,
        scope=SCOPES[0],
        user_agent='app.testing',
        access_token=credentials.token,
        refresh_token=credentials.refresh_token,
    )
    contact_client = gdata.contacts.client.ContactsClient()
    token.authorize(contact_client)
    feed = contact_client.GetContacts()
    for entry in feed.entry:
        print(entry.title.text)
        for e in entry.email:
            print("\t"+e.address)
