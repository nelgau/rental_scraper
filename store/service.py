# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from store.models import Rental, db_connect, create_tables, drop_tables
from itertools import groupby
import collections

class Service(object):
    def __init__(self):
        self.engine = db_connect()                
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        create_tables(self.engine)

    def drop_tables(self):
        drop_tables(self.engine)

    def store_search_result(self, result_item):
        session = self.Session()

        crawl_timestamp = result_item.get('crawl_timestamp')
        parse_timestamp = result_item.get('parse_timestamp')
        url = result_item.get('url')

        attributes = dict(result_item)
        del attributes['crawl_timestamp']
        del attributes['parse_timestamp']
        was_inserted = False

        try:
            instance = session.query(Rental).filter_by(url=url).first()

            if instance is not None:
                instance.last_seen_at = parse_timestamp
                instance.off_market_at = None
                for k, v in attributes.items():
                    setattr(instance, k, v)
                session.flush()
            else:
                instance = Rental(**attributes)
                instance.first_crawl_at = crawl_timestamp
                instance.first_seen_at = parse_timestamp
                instance.last_seen_at = parse_timestamp
                session.add(instance)
                was_inserted = True
                
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return was_inserted

    def get_search_results(self):
        session = self.Session()
        try:
            results = session.query(Rental).all()
            results.sort(key=lambda r: [r.first_crawl_at, r.first_seen_at], reverse=True)
            return [i.__dict__ for i in results]
        finally:
            session.close()

    def get_search_results_for_web(self, nh_id=None):
        session = self.Session()
        try:
            query = session.query(Rental)
            if nh_id:
                query = query.filter(Rental.neighborhood_id == nh_id)
            results = query.all()
            grouped_dict = collections.defaultdict(list)
            for r in results:
                grouped_dict[r.first_crawl_at].append(r)
            grouped_pairs = list(grouped_dict.items())
            grouped_pairs.sort(key=lambda x: x[0], reverse=True)
            for k, g in grouped_pairs:
                g.sort(key=lambda x: x.first_seen_at, reverse=True)
            return grouped_pairs
        finally:
            session.close()
