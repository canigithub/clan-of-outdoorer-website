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