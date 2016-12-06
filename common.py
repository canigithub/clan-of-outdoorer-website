from functools import wraps
from flask import session, request, redirect, url_for


def login_required(f):
   '''
   if user is not logged-in, redirect to login page
   '''
   @wraps(f)
   def func(*args, **kwargs):
      if 'name' not in session:
         return redirect(url_for('userview.route_loginpage'))
      return f(*args, **kwargs)
   return func



def already_loggedin_redirect(f):
   '''
   if user is logged-in, redirect to all-categories page
   '''
   @wraps(f)
   def func(*a, **kw):
      if 'name' in session:
         return redirect(url_for('userview.route_logoutpage'))
      return f(*a, **kw)
   return func