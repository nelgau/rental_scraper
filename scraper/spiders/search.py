# -*- coding: utf-8 -*-
import os
import scrapy
from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy.linkextractors import LinkExtractor
import js2xml

from scraper.parsing import core_property_url
from scraper.items import SearchResultItemLoader
from store.models import Neighborhood

import re
import datetime
from pprint import pprint

class SearchSpider(Spider):
    name = 'search'
    allowed_domains = ['trulia.com']

    custom_settings = {
        'DOWNLOAD_DELAY': 30,
        'CONCURRENT_REQUESTS': 1,
        'ITEM_PIPELINES': {
            'scraper.pipelines.StoreSearchResultPipeline': 400
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crawl_timestamp = datetime.datetime.utcnow()
        self.le = LinkExtractor(allow=r'^https://www.trulia.com/for_rent/.+/[\d]+_p/')

    def start_requests(self):        
        for nh in Neighborhood.all():
            url = self.build_search_url(nh.nh_id)
            yield Request(url, meta={'nh_id': nh.nh_id}, dont_filter=True)

    def build_search_url(self, nh_id):
        url = 'https://www.trulia.com/for_rent/{nh_id}_nh'.format(nh_id=nh_id)
        url += '/2p_beds'
        url += '/3000-4500_price'
        url += '/'
        return url

    def parse(self, response):    
        nh_id = response.meta['nh_id']
        for link in self.le.extract_links(response):
            yield Request(url=link.url, meta={'nh_id': nh_id}, callback=self.parse)

        app_state = self.load_app_state(response)
        card_index = self.build_card_index(app_state)

        for selector in response.css('div.card'):
          item = self.load_search_result_item(selector, response, card_index)
          if item and item.is_basic_rental():
            yield item          

    def load_app_state(self, response):
        text = self.find_app_state_text(response)
        if text is None:
            self.logger.debug("Couldn't find app state script, continuing...")
            return {}

        try:
            text_jstree = js2xml.parse(text)
            object_jstree = text_jstree.xpath('//var[@name="appState"]/object')[0]
            return js2xml.jsonlike.make_dict(object_jstree)
        except (IndexError, ValueError, TypeError, AttributeError) as err:
          self.logger.debug("Error parsing app state script: %s", err)
          return {}

    def find_app_state_text(self, response):
        for selector in response.css('script'):
            text = selector.css('::text').get()
            if text and re.search('var appState', text):
                return text
        return None

    def build_card_index(self, app_state):
        card_index = {}
        try:
            for card in app_state['page']['cards']:
                url = card['cardUrl']
                card_index[url] = card
        except (IndexError, ValueError, TypeError, AttributeError) as err:
            self.logger.debug("Error buiding card index: %s", err)
        finally:
            return card_index

    def get_photo_url(self, card):
        if 'photoUrlForHdDpiDisplay' in card:
            return card['photoUrlForHdDpiDisplay']
        elif 'photoUrl' in card:
            return card['photoUrl']
        else:
            return None

    def load_search_result_item(self, selector, response, card_index):        
        loader = SearchResultItemLoader(selector=selector, response=response)

        loader.add_value('crawl_timestamp', self.crawl_timestamp)
        loader.add_value('parse_timestamp', datetime.datetime.utcnow())

        loader.add_value('neighborhood_id', response.meta['nh_id'])
        loader.add_value('referrer_url', response.url)

        url = selector.css('a.tileLink:first-child::attr(href)').get()
        core_url = core_property_url(url)
        if core_url is None:
            return None

        loader.add_value('url', core_url)

        card = card_index.get(url)
        if card:
            thumbnail_url = self.get_photo_url(card)
            if thumbnail_url:
                loader.add_value('thumbnail_url', thumbnail_url)

        # Jump out beyond the selector to capture global data
        neighborhood = response.css('div.locationCardContent > span.locationCardHero > img::attr(alt)').get()
        loader.add_value('neighborhood', neighborhood)

        address = selector.css('span[itemprop="streetAddress"]::text').get()
        if address != neighborhood:
            loader.add_value('address', address)
              
        loader.add_css('city', 'span[itemprop="addressLocality"]::text')
        loader.add_css('state', 'span[itemprop="addressRegion"]::text')
        loader.add_css('zipcode', 'span[itemprop="postalCode"]::text')
        loader.add_css('latitude', 'meta[itemprop="latitude"]::attr(content)')
        loader.add_css('longitude', 'meta[itemprop="longitude"]::attr(content)')

        loader.add_css('price', 'span.cardPrice::text', re=r'\$([\d,]+)')
        loader.add_css('sqft', 'li[data-testid="sqft"]::text', re=r'([\d,]+) sqft$')
        loader.add_css('bedrooms', 'li[data-testid="beds"]::text', re=r'(\d+)bd$')
        loader.add_css('bathrooms', 'li[data-testid="baths"]::text', re=r'(\d+)ba$')

        tags = set(selector.css('div.tagsListContainer > ul.tags > li::text').getall())
        loader.add_value('pet_friendly', 'Pet Friendly' in tags)
        loader.add_value('furnished', 'Furnished' in tags)

        return loader.load_item()
