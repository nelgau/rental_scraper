# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Identity, Compose
from scraper.parsing import urljoin_to_context

import re

class SearchResultItem(scrapy.Item):
    crawl_timestamp = scrapy.Field()
    parse_timestamp = scrapy.Field()

    url = scrapy.Field()
    thumbnail_url = scrapy.Field()
    referrer_url = scrapy.Field()

    neighborhood_id = scrapy.Field()
    neighborhood = scrapy.Field()
    
    address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()    
    zipcode = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()

    price = scrapy.Field()
    sqft = scrapy.Field()
    bedrooms = scrapy.Field()
    bathrooms = scrapy.Field()

    pet_friendly = scrapy.Field()
    furnished = scrapy.Field()

    def is_basic_rental(self):
        return re.match(r'^https://www.trulia.com/p/', self.get('url'))

class SearchResultItemLoader(ItemLoader):
    default_item_class = SearchResultItem

    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()

    crawl_timestamp_in = Identity()
    parse_timestamp_in = Identity()

    neighborhood_id_in = Identity()    
    url_in = MapCompose(urljoin_to_context)

    latitude_out = Compose(TakeFirst(), float)
    longitude_out = Compose(TakeFirst(), float)

    price_out = Compose(TakeFirst(), lambda s: int(s.replace(',', '')))
    sqft_out = Compose(TakeFirst(), lambda s: int(s.replace(',', '')))
    bedrooms_out = Compose(TakeFirst(), int)
    bathrooms_out = Compose(TakeFirst(), int)

    pet_friendly_in = Identity()
    furnished_in = Identity()
