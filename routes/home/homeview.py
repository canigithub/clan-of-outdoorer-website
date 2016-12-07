from flask import Blueprint, render_template, abort, session
from jinja2 import TemplateNotFound

homeview = Blueprint('homeview', __name__)

@homeview.route('/')
def route_homepage():
   try:
     return render_template('homepage.html')
   except TemplateNotFound:
     abort(404)


@homeview.route('/welcome')
def route_welcomepage():
   return render_template('welcome.html')


@homeview.route('/catalog')
def route_catalogpage():
   items = []
   items.append(CataItem('Hiking', 'static/img/cata-it-img-hiking.jpg',
      'hiking', '/catalog/hiking'))
   items.append(CataItem('Mountain Biking', 'static/img/cata-it-img-biking.jpg',
      'mountain biking', '/catalog/biking'))
   items.append(CataItem('Snow Sports', 'static/img/cata-it-img-snow.jpg',
    'snow sports', '/catalog/snow'))
   items.append(CataItem('Rock Climbing', 'static/img/cata-it-img-rock.jpg',
      'rock climbing', '/catalog/rock'))
   items.append(CataItem('Kayaking', 'static/img/cata-it-img-kayaking.jpg',
      'kayaking', '/catalog/kayaking'))
   items.append(CataItem('Camping', 'static/img/cata-it-img-camping.jpg',
      'camping', '/catalog/camping'))
   items.append(CataItem('Diving', 'static/img/cata-it-img-diving.jpg',
      'diving', '/catalog/diving'))
   items.append(CataItem('Skydiving', 'static/img/cata-it-img-skydiving.jpg',
      'skydiving', '/catalog/skydiving'))
   items.append(CataItem('Fishing', 'static/img/cata-it-img-fishing.jpg',
      'fishing', '/catalog/fishing'))
   return render_template('catalog.html', cata_items=items)




class CataItem():
   '''
   CataItem: contain contents of items on catalog page.
   '''
   def __init__(self, title, img_url, alt, link_url):
      self.title = title
      self.img_url = img_url
      self.alt = alt
      self.link_url = link_url


   def render(self):
      '''
      render the html for the current item
      '''
      return render_template('cataitem.html', title=self.title, img_url=self.img_url,
         alt=self.alt, link_url=self.link_url)