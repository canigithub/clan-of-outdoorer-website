import hashlib
import random
from string import letters

from google.appengine.ext import db

SALT_LEN = 10

##### Helper Functions

def hash_str(s):
   """
   genrate hash string use sha256 hashing algorithm
   """
   return hashlib.sha256(s).hexdigest()


def make_salt():
   """
   generate a random SALT_LEN character string
   """
   return ''.join(random.SystemRandom().choice(letters) for x in xrange(SALT_LEN))


def make_passwd_hash(username, passwd, salt=None):
   """
   encode as: hash(username + passwd + salt)
   return 'salt,hash_str'
   """
   if not salt:
      salt = make_salt()
   h = hash_str(username + passwd + salt)
   return '%s,%s' % (salt, h)


def valid_pw(username, passwd, h):
   """
   check if username, passwd pair is valid
   """
   salt = h.split(',')[0]
   return h == make_passwd_hash(username, passwd, salt)



##### #####

def user_key(group='default'):
   """
   genrate parent key.
   ensure hierarchy for future use.
   default parent key: Key('users', 'default')
   """
   return db.Key.from_path('users', group)



##### Model - User

class User(db.Model):
   """
   Model - User:
      username - username
      pw_hash - hased password
      email - email
   """
   username = db.StringProperty()
   pw_hash = db.StringProperty()
   email = db.StringProperty()



   @classmethod
   def by_id(cls, uid):
      """
      get object using id
      """
      return cls.get_by_id(int(uid), parent=user_key())


   @classmethod
   def by_username(cls, username):
      """
      get object using 'username' field
      """
      return cls.all().filter("username =", username).get()


   @classmethod
   def by_email(cls, email):
      """
      get object using 'email' field
      """
      return cls.all().filter("email =", email).get()


   @classmethod
   def create(cls, username=None, passwd=None, email=None):
      """
      create a new User object
      """
      pw_hash=None
      if username and passwd:
         pw_hash = make_passwd_hash(username, passwd)
      return cls(parent=user_key(), username=username, pw_hash=pw_hash, email=email)


   @classmethod
   def verify_username_passwd(cls, username, passwd):
      """
      check if username + passwd is valid. if valid,
      return the User object
      """
      u = cls.by_username(username)
      if u and valid_pw(username, passwd, u.pw_hash):
         return u




