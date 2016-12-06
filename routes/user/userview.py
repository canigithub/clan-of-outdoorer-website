import re, json, random, string, time

from flask import Blueprint, render_template, abort, url_for, request, redirect, session, flash

from models.user_model import User
import common

# for 3rd party sign-in
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

# import oauth2client
import httplib2
import json
from flask import make_response
import requests


userview = Blueprint('userview', __name__)

STATE_LEN = 32

##### Helper Functions

USER_RE = re.compile(r'^[\w-]{3,20}$')
def valid_username(username):
   """
   username: 3-20 non-whitespace chars
   check if username is a valid format
   """
   return username and USER_RE.match(username)


PASSWD_RE = re.compile(r'^.{3,20}$')
def valid_password(password):
   """
   password: 3-20 chars
   check if password is a valid format
   """
   return password and PASSWD_RE.match(password)


# EMAIL_RE = re.compile(r'^\S+@\S+\.\S+$')
# def valid_email(email):
#    """
#    check if email is a valid format
#    """
#    return email and EMAIL_RE.match(email)



##### Routes for user signup, login, logout

@userview.route('/signup', methods=['GET', 'POST'])
@common.already_loggedin_redirect
def route_signuppage():

   # protect website from anti-forgery request attack from malicious scripts
   state = ''.join(random.SystemRandom().choice(string.letters) for x in xrange(STATE_LEN))
   session['state'] = state

   if request.method == 'GET':
      return render_template('user/signup.html', state=state)

   elif request.method == 'POST':
      username = request.form['username']
      if not valid_username(username):
         return render_template('user/signup.html', state=state, error_msg='username must be 3-20 non-whitespace characters')

      password = request.form['password']
      if not valid_password(password):
         return render_template('user/signup.html', state=state, error_msg='password must be 3-20 characters')

      verify = request.form['verify']
      if password != verify:
         return render_template('user/signup.html', state=state, error_msg='passwords not match')

      if User.by_username(username):
         return render_template('user/signup.html', state=state, error_msg='username already exists')

      user = User.create(username=username, passwd=password)
      user.put()

      session['name'] = username
      session['user_id'] = user.key().id()
      session['provider'] = 'myweb'

      # TODO: modify here to redirect to login
      return redirect(url_for('homeview.route_welcomepage'))

   else:
      abort(405)  # method not allowed


@userview.route('/login', methods=['GET', 'POST'])
@common.already_loggedin_redirect
def route_loginpage():

   # protect website from anti-forgery request attack from malicious scripts
   state = ''.join(random.SystemRandom().choice(string.letters) for x in xrange(STATE_LEN))
   session['state'] = state

   if request.method == 'GET':
      return render_template('/user/login.html', state=state)

   elif request.method == 'POST':
      username = request.form['username']
      password = request.form['password']

      user = User.verify_username_passwd(username, password)
      if not user:
         return render_template('/user/login.html', state=state, error_msg='username and password not match')

      session['name'] = username
      session['user_id'] = user.key().id()
      session['provider'] = 'myweb'

      return redirect(url_for('homeview.route_welcomepage'))

   else:
      abort(405)  # method not allowed


@userview.route('/logout', methods=['GET', 'POST'])
@common.login_required
def route_logoutpage():
   if request.method == 'GET':
      print("login-type:", session['provider'])
      return render_template('/user/logout.html', provider=session['provider'])

   elif request.method == 'POST':
      session.pop('name')
      session.pop('user_id')
      # TODO: add flash

      time.sleep(3)
      return redirect(url_for('homeview.route_homepage'))

   else:
      abort(405)  # method not allowed



@userview.route('/third-party-connect', methods=['POST'])
@common.already_loggedin_redirect
def route_gconnect():
   print('start:', session)

   # Validate state token
   if 'state' not in session or session['state'] != request.args.get('state'):
      response = make_response(json.dumps('Invalid state parameter.'), 401)
      response.headers['Content-Type'] = 'application/json'
      print "state and state don't match."
      return response

   data = json.loads(request.data)


   provider = data['provider']
   name = data['name']

   if provider == 'google':
      # name += '_g'
      email = data['email']
   elif provider == 'facebook':
      # facebook doesn't provide email. so I make one.
      # name += '_f'
      email = data['id'] + '@facebook.facebook'
      session['access_token'] = data['access_token']
   else:
      response = make_response(json.dumps(result.get('error')), 405)
      response.headers['Content-Type'] = 'application/json'
      return response

   user = User.by_email(email)
   if not user:
      user = User.create(email=email)
      user.put()

   session['name'] = name
   session['user_id'] = user.key().id()
   session['provider'] = provider

   flash("you are now logged in as %s" % session['name'])

   print('end:', session)
   return "done!"









