import pytest
import unittest
from doodledashboard.component import MissingRequiredOptionException

from doodledashboard.datafeeds.datafeed import Message
from doodledashboard.filters.matches_regex import MatchesRegexFilter, MatchesRegexFilterCreator


class TestConfig(unittest.TestCase):
    _EMPTY_OPTIONS = {}
    _EMPTY_SECRET_STORE = {}

    def test_id_is_message_matches_regex(self):
        self.assertEqual("message-matches-regex", MatchesRegexFilterCreator.get_id())

    def test_exception_raised_when_no_pattern_in_options(self):
        with pytest.raises(MissingRequiredOptionException) as err_info:
            MatchesRegexFilterCreator().create(self._EMPTY_OPTIONS, self._EMPTY_SECRET_STORE)

        self.assertEqual("Expected 'pattern' option to exist", err_info.value.message)


class TestFilter(unittest.TestCase):

    def test_regex_matches_single_message(self):
        message = Message('test1 test2')
        self.assertTrue(MatchesRegexFilter('test1|test3').filter(message))

    def test_regex_matches_multiple_messages(self):
        message = Message('test 2')
        self.assertFalse(MatchesRegexFilter('test1|test3').filter(message))

    def test_regex_does_not_match(self):
        message = Message('test1 test2')
        self.assertFalse(MatchesRegexFilter('test3').filter(message))


if __name__ == '__main__':
    unittest.main()
