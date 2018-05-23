import feedparser

from doodledashboard.configuration.config import MissingRequiredOptionException
from doodledashboard.datafeeds.datafeed import DataFeed, TextEntity, DataFeedConfigSection


class RssFeed(DataFeed):
    _COMMON_RSS_ITEM_FIELDS = ["title", "link", "description", "published", "id"]

    def __init__(self, url):
        DataFeed.__init__(self)
        self._feed_url = url

    def get_url(self):
        return self._feed_url

    def get_latest_entities(self):
        feed = feedparser.parse(self._feed_url)
        return [self._convert_to_message(item) for item in feed.entries]

    def __str__(self):
        return "RSS feed for %s" % self._feed_url

    def _convert_to_message(self, feed_item):
        feed_fields = []

        for field in RssFeed._COMMON_RSS_ITEM_FIELDS:
            if field in feed_item:
                feed_fields.append(feed_item[field])

        return TextEntity("\n".join(feed_fields), self)


class RssFeedSection(DataFeedConfigSection):
    def __init__(self):
        DataFeedConfigSection.__init__(self)

    def creates_for_id(self, filter_id):
        return filter_id == "rss"

    def create_item(self, config_section):
        if "url" not in config_section:
            raise MissingRequiredOptionException("Expected 'url' option to exist")

        return RssFeed(config_section["url"])
