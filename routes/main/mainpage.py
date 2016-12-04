from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

mainpage = Blueprint('mainpage', __name__)

@mainpage.route('/')
def mainpage():
   try:
     return render_template('mainpage.html')
   except TemplateNotFound:
     abort(404)