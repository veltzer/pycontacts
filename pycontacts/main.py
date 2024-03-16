"""
main
"""
from typing import Generator, Union

import pylogconf.core
from gdata.client import RequestError
from gdata.contacts import ContactEntry

from pygooglehelper import register_functions, ConfigRequest, get_credentials

from pytconf import register_endpoint, register_main, config_arg_parse_and_launch

import gdata.data
import gdata.gauth
import gdata.contacts.client
import gdata.contacts.data

from pycontacts.configs import ConfigAuthFiles, ConfigFix
from pycontacts.static import APP_NAME, DESCRIPTION, VERSION_STR

from pycontacts.utils import dump

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    "https://www.googleapis.com/auth/contacts",
]


def get_token():
    credentials = get_credentials()
    token = gdata.gauth.OAuth2Token(
        client_id=credentials.client_id,
        client_secret=credentials.client_secret,
        scope=SCOPES[0],
        user_agent=APP_NAME,
        access_token=credentials.token,
        refresh_token=credentials.refresh_token,
    )
    return token


@register_endpoint(
    configs=[ConfigAuthFiles],
    description="Dump full info for all contacts",
)
def dump_contacts() -> None:
    token = get_token()
    contacts_client = gdata.contacts.client.ContactsClient(auth_token=token)
    for entry in yield_all_entries(contacts_client):
        dump(entry)


def yield_all_entries(contacts_client) -> Generator[ContactEntry, None, None]:
    query = gdata.contacts.client.ContactsQuery()
    # see all parameters in :py:class:`gdata.query.ContactsQuery`
    query.strict = True
    # default is 25, too slow
    query.max_results = 500
    query.start_index = 0
    while True:
        feed = contacts_client.GetContacts(q=query)
        if len(feed.entry) == 0:
            break
        query.start_index += len(feed.entry)
        yield from feed.entry


@register_endpoint(
    configs=[ConfigAuthFiles, ConfigFix],
    description="Fix the phone numbers so that parsed form equals presentation form",
)
def fix_phones():
    token = get_token()
    contacts_client = gdata.contacts.client.ContactsClient(auth_token=token)
    for entry in yield_all_entries(contacts_client):
        numbers = entry.phone_number
        for i, number in enumerate(numbers):
            if not is_special_phone(entry, number):
                if number.uri is None:
                    print(f"problem with [{get_summary(entry)}] [{number.text}]")
                    continue
                formatted = number.uri.split(":")[1]
                if number.text != formatted:
                    print(f"fixing [{number.text}] ->[{formatted}]")
                    if ConfigFix.doit:
                        entry.phone_number[i].text = formatted
                        try:
                            contacts_client.update(entry)
                        except RequestError:
                            print("failed to update")


@register_endpoint(
    configs=[ConfigAuthFiles],
    description="Show phones that google can't parse or are just weird",
)
def show_bad_phones():
    token = get_token()
    contacts_client = gdata.contacts.client.ContactsClient(auth_token=token)
    for entry in yield_all_entries(contacts_client):
        numbers = entry.phone_number
        for number in numbers:
            if is_bad_phone(entry, number):
                print(f"[{get_summary(entry)}] [{number.text}]")


# noinspection PyUnresolvedReferences
def unfilled_contact(entry: ContactEntry) -> bool:
    """
    A contact which is unfilled is one which does not have
    neither name or family name
    :param entry:
    :return:
    """
    if entry.email is not None:
        if len(entry.email) >= 1:
            if entry.email[0].address is not None:
                return False
    if entry.name is not None:
        if entry.name.given_name is not None:
            return False
        if entry.name.family_name is not None:
            return False
    if entry.organization is not None:
        if entry.organization.name is not None:
            if entry.organization.name.text is not None:
                return False
        if entry.organization.department is not None:
            if entry.organization.department.text is not None:
                return False
    return True


@register_endpoint(
    configs=[ConfigAuthFiles],
    description="Show contacts that don't have the main fields filled",
)
def unfilled_contacts_show():
    token = get_token()
    contacts_client = gdata.contacts.client.ContactsClient(auth_token=token)
    for entry in yield_all_entries(contacts_client):
        if unfilled_contact(entry):
            dump(entry)


@register_endpoint(
    configs=[ConfigAuthFiles],
    description="Delete contacts that don't have the main fields filled",
)
def unfilled_contacts_delete():
    token = get_token()
    contacts_client = gdata.contacts.client.ContactsClient(auth_token=token)
    for entry in yield_all_entries(contacts_client):
        if unfilled_contact(entry):
            contacts_client.delete(entry)


def is_bad_phone(entry, number) -> bool:
    if number.uri is None:
        if is_special_phone(entry, number):
            return False
        return True
    return False


def is_special_phone(entry, number) -> bool:
    if (
        entry.organization is not None
        and number.text.startswith("*")
        and 4 <= len(number.text) <= 5
    ):
        return True
    if (
        entry.organization is not None
        and number.text.startswith("1")
        and len(number.text) == 3
    ):
        return True
    return False


def get_summary(entry) -> Union[None, str]:
    show = None
    if entry.title.text is not None:
        show = f"title:{entry.title.text}"
    if entry.organization is not None:
        show = f"organization:{entry.organization.name.text}"
    return show


@register_main(
    main_description=DESCRIPTION,
    app_name=APP_NAME,
    version=VERSION_STR,
)
def main():
    pylogconf.core.setup()
    ConfigRequest.app_name = APP_NAME
    ConfigRequest.scopes = SCOPES
    register_functions()
    config_arg_parse_and_launch()


if __name__ == "__main__":
    main()
