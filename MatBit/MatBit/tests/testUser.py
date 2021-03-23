import MySQLdb
import django
from django.test import TestCase
from django.core.exceptions import ValidationError
from MatBit.MatBit.views import add_user as _add_user


class UserTestCase(TestCase):
    def setUp(self):
        pass

    @staticmethod
    def _add_user_suppressing_database_issues(*args):
        try:
            _add_user(*args)
        except MySQLdb._exceptions.ProgrammingError or django.db.utils.ProgrammingError:
            pass

    def test_add_user(self):
        add_user = UserTestCase._add_user_suppressing_database_issues
        # Shall not fail
        add_user(
            "George",
            "Lucas",
            "2000-01-01",
            "Somewhere in the US",
            "3423",
            "Somewhere else, I guess",
            False,
            "george@lucas.org",
            "Star Wars is best"
        )

        # Birth date
        self.assertRaises(ValidationError, lambda: add_user(
            "George",
            "Lucas",
            "2000-01-01",
            "Somewhere in the US",
            "3423",
            "Somewhere else, I guess",
            False,
            "not a valid e-mail",
            "Star Wars is best"
        ))

        # Birth date (too young)
        self.assertRaises(ValidationError, lambda: add_user(
            "George",
            "Lucas",
            "2020-07-25",
            "Somewhere in the US",
            "3423",
            "Somewhere else, I guess",
            False,
            "not a valid e-mail",
            "Star Wars is best"
        ))

        # Post code
        self.assertRaises(ValidationError, lambda: add_user(
            "George",
            "Lucas",
            "2000-01-01",
            "Somewhere in the US",
            "Not a post code",
            "Somewhere else, I guess",
            False,
            "george@lucas.org",
            "Star Wars is best"
        ))

        # E-mail
        self.assertRaises(ValidationError, lambda: add_user(
            "George",
            "Lucas",
            "2000-01-01",
            "Somewhere in the US",
            "3423",
            "Somewhere else, I guess",
            False,
            "not a valid e-mail",
            "Star Wars is best"
        ))
