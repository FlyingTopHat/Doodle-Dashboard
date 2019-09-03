import unittest

from doodledashboard.component import ComponentConfig, DataFeedConfig
from doodledashboard.configuration import ComponentConfigParser
from doodledashboard.datafeeds.datafeed import DataFeed


class DummyFeed(DataFeed):

    def __init__(self, options):
        super().__init__()
        self.options = options

    def get_latest_messages(self):
        return []


class DummyFeedConfig(ComponentConfig, DataFeedConfig):

    @staticmethod
    def get_id():
        return "test-feed"

    def create(self, options):
        return DummyFeed(options)


class TestComponentConfigParser(unittest.TestCase):

    def test_name_is_set_against_component(self):
        abc = ComponentConfigParser([DummyFeedConfig()])
        component = abc.parse({
            'name': 'test-name',
            'type': 'test-feed',
            'options': {
                'option-1': 'test-value-1'
            }
        })

        self.assertEqual(component.name, 'test-name')
        self.assertEqual(component.options, {
            'option-1': 'test-value-1'
        })

    def test_options_are_passed_to_create_method_of_config(self):
        abc = ComponentConfigParser([DummyFeedConfig()])
        component = abc.parse({
            'type': 'test-feed',
            'options': {
                'option-1': 'test-value-1'
            }
        })

        self.assertEqual(component.options, {
            'option-1': 'test-value-1'
        })


if __name__ == '__main__':
    unittest.main()
