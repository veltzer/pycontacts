"""
The default group of operations that pycontacts has
"""
import logging
import os.path
import pickle
from typing import Generator

from gdata.contacts import ContactEntry
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

from pycontacts.utils import dump

GROUP_NAME_DEFAULT = "default"
GROUP_DESCRIPTION_DEFAULT = "all pycontacts commands"

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/contacts.readonly',
]
APP_NAME = "pycontacts"


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
def list_contacts() -> None:
    """ List all contacts """
    token = get_token()
    for entry in yield_all_entries(token):
        dump(entry)


def yield_all_entries(token) -> Generator[ContactEntry, None, None]:
    query = gdata.contacts.client.ContactsQuery()
    # see all parameters in :py:class:`gdata.query.ContactsQuery`
    query.strict = True
    # default is 25, too slow
    query.max_results = 500
    query.start_index = 0
    contacts_client = gdata.contacts.client.ContactsClient(auth_token=token)
    while True:
        feed = contacts_client.GetContacts(q=query)
        if len(feed.entry) == 0:
            break
        query.start_index += len(feed.entry)
        for entry in feed.entry:
            yield entry


@register_endpoint(
    configs=[
        ConfigAuthFiles,
    ],
)
def fix_phones():
    """ Fix the phone numbers in my contacts """
    nones = 0
    texts = []
    token = get_token()
    for entry in yield_all_entries(token):
        numbers = entry.phone_number
        for number in numbers:
            if number.uri is None:
                nones += 1
                texts.append(number.text)
            else:
                formatted = number.uri.split(":")[1]
                if number.text != formatted:
                    print("diff {} {}".format(number.text, formatted))
    print("got [{}] nones".format(nones))
    print(texts)


@register_endpoint(
    configs=[
        ConfigAuthFiles,
    ],
)
def show_bad_phones():
    """ Show bad phones """
    nones = 0
    texts = []
    token = get_token()
    for entry in yield_all_entries(token):
        numbers = entry.phone_number
        for number in numbers:
            if number.uri is None:
                if entry.organization is not None and number.text.startswith("*") and len(number.text) == 4:
                    continue
                if entry.organization is not None and number.text.startswith("1") and len(number.text) == 3:
                    continue
                show = None
                if entry.title.text is not None:
                    show = "title:{}".format(entry.title.text)
                if entry.organization is not None:
                    show = "organization:{}".format(entry.organization.name.text)
                print("[{}] [{}]".format(show, number.text))


def get_token():
    logger = logging.getLogger(pycontacts.LOGGER_NAME)
    credentials = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.access(ConfigAuthFiles.token, os.R_OK):
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
        logger.info("creating a new token file")
        if os.access(ConfigAuthFiles.token, os.R_OK):
            os.unlink(ConfigAuthFiles.token)
        with open(ConfigAuthFiles.token, 'wb') as token:
            pickle.dump(credentials, token)
        os.chmod(ConfigAuthFiles.token, 0o400)
    # flat_dump(credentials)
    token = gdata.gauth.OAuth2Token(
        client_id=credentials.client_id,
        client_secret=credentials.client_secret,
        scope=SCOPES[0],
        user_agent=APP_NAME,
        access_token=credentials.token,
        refresh_token=credentials.refresh_token,
    )
    return token
