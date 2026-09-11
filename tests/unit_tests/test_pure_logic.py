"""Behavioural tests for pycontacts' pure logic.

The phone classification and contact-emptiness predicates in main.py
operate on duck-typed gdata entries, so plain namespaces with the
same attributes stand in for real ContactEntry objects. utils holds
a pure object-to-value helper.
"""

import types
import unittest

from pycontacts import utils
from pycontacts.main import get_summary, is_bad_phone, is_special_phone, unfilled_contact


def _ns(**kwargs: object) -> types.SimpleNamespace:
    return types.SimpleNamespace(**kwargs)


class ObjectDumpHelperTests(unittest.TestCase):
    def test_object_with_dict_returns_vars(self) -> None:
        obj = _ns(a=1, b="x")
        self.assertEqual(utils.object_to_members_or_string(obj), {"a": 1, "b": "x"})

    def test_plain_value_returns_str(self) -> None:
        self.assertEqual(utils.object_to_members_or_string(5), "5")


class SpecialPhoneTests(unittest.TestCase):
    def test_star_code_with_org_is_special(self) -> None:
        entry = _ns(organization=_ns())
        number = _ns(text="*100")
        self.assertTrue(is_special_phone(entry, number))

    def test_short_one_code_with_org_is_special(self) -> None:
        entry = _ns(organization=_ns())
        number = _ns(text="103")
        self.assertTrue(is_special_phone(entry, number))

    def test_no_organization_is_not_special(self) -> None:
        entry = _ns(organization=None)
        number = _ns(text="*100")
        self.assertFalse(is_special_phone(entry, number))

    def test_regular_number_is_not_special(self) -> None:
        entry = _ns(organization=_ns())
        number = _ns(text="0501234567")
        self.assertFalse(is_special_phone(entry, number))


class BadPhoneTests(unittest.TestCase):
    def test_missing_uri_and_not_special_is_bad(self) -> None:
        entry = _ns(organization=None)
        number = _ns(text="0501234567", uri=None)
        self.assertTrue(is_bad_phone(entry, number))

    def test_present_uri_is_not_bad(self) -> None:
        entry = _ns(organization=None)
        number = _ns(text="0501234567", uri="tel:+972501234567")
        self.assertFalse(is_bad_phone(entry, number))

    def test_missing_uri_but_special_is_not_bad(self) -> None:
        entry = _ns(organization=_ns())
        number = _ns(text="*100", uri=None)
        self.assertFalse(is_bad_phone(entry, number))


class UnfilledContactTests(unittest.TestCase):
    def test_contact_with_email_is_filled(self) -> None:
        entry = _ns(email=[_ns(address="a@b.com")], name=None, organization=None)
        self.assertFalse(unfilled_contact(entry))

    def test_contact_with_given_name_is_filled(self) -> None:
        entry = _ns(email=None, name=_ns(given_name="Ada", family_name=None), organization=None)
        self.assertFalse(unfilled_contact(entry))

    def test_empty_contact_is_unfilled(self) -> None:
        entry = _ns(email=None, name=None, organization=None)
        self.assertTrue(unfilled_contact(entry))


class GetSummaryTests(unittest.TestCase):
    def test_organization_overrides_title(self) -> None:
        entry = _ns(title=_ns(text="Mr"), organization=_ns(name=_ns(text="Acme")))
        self.assertEqual(get_summary(entry), "organization:Acme")

    def test_title_used_when_no_organization(self) -> None:
        entry = _ns(title=_ns(text="Mr"), organization=None)
        self.assertEqual(get_summary(entry), "title:Mr")

    def test_none_when_nothing_present(self) -> None:
        entry = _ns(title=_ns(text=None), organization=None)
        self.assertIsNone(get_summary(entry))


if __name__ == "__main__":
    unittest.main()
