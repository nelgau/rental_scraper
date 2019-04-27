from flask import Blueprint, render_template, flash, request, redirect, url_for

from store.service import Service
from store.models import Neighborhood, NeighborhoodGroup

from datetime import datetime, timezone
from pprint import pprint
from six.moves.urllib.parse import urljoin
import pytz
import humanize

rentals = Blueprint('rentals', __name__)
service = Service()

@rentals.route('/')
@rentals.route('/n/<int:nh_id>')
def index(nh_id=None):    
    grouped_rentals = service.get_search_results_for_web(nh_id=nh_id)
    presented = present_grouped_rentals(grouped_rentals)
    nh_query = get_nh_query_description(nh_id)
    nh_groups = NeighborhoodGroup.all()    
    return render_template('rentals.html', presented=presented, nh_query=nh_query, nh_groups=nh_groups)

def get_nh_query_description(nh_id):
    return Neighborhood.by_id(nh_id).name if nh_id else 'All Neighborhoods'

def string_date(dt):
    pacific_tz = pytz.timezone('US/Pacific')
    return dt.replace(tzinfo=timezone.utc).astimezone(tz=pacific_tz).strftime('%a, %B %d \u2014 %l:%M %p')

def relative_date(dt):
    relative = datetime.now() - dt
    return humanize.naturaltime(relative)

def present_grouped_rentals(grouped):
    return [[
        string_date(dt),
        relative_date(dt),
        [RentalPresenter(r) for r in g
    ]] for dt, g in grouped]

class RentalPresenter(object):
    def __init__(self, ro):
        self.ro = ro

    def url(self):
        return self.ro.url

    def thumbnail_url(self):
        if self.ro.thumbnail_url:
            return urljoin('https://thumbs.trulia-cdn.com', self.ro.thumbnail_url)
        else:
            return ''

    def price(self):
        return '${price:,}'.format(price=self.ro.price) if self.ro.price else '\xa0'

    def address(self):
        return self.ro.address if self.ro.address else '\xa0'

    def neighborhood(self):
        if self.ro.neighborhood and self.ro.city:
          return '{nh}, {city}'.format(nh=self.ro.neighborhood, city=self.ro.city)
        else:
          return '\xa0'

    def has_bedrooms(self):
        return self.ro.bedrooms is not None

    def bedrooms(self):
        return self.ro.bedrooms

    def has_bathrooms(self):
        return self.ro.bathrooms is not None

    def bathrooms(self):
        return self.ro.bathrooms

    def has_sqft(self):
        return self.ro.sqft is not None

    def sqft(self):
        return '{sqft:,}'.format(sqft=self.ro.sqft) if self.ro.sqft else '\xa0'

    def tags(self):
        tags = []
        if self.ro.pet_friendly:
            tags.append('Pet Friendly')
        if self.ro.furnished:
            tags.append('Furnished')
        return tags
