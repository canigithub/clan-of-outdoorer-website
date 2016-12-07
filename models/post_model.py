from google.appengine.ext import db

from user_model import User

from flask import render_template

##### #####

def post_key(name='default'):
   """
   ensure hierarchy for future use.
   default parent key: Key('posts', 'default')
   """
   return db.Key.from_path('posts', name)



##### Model - Post

class Post(db.Model):
   """
   Model - Post:
      user - foreign key to User
      title - title of the post
      content - content of the post
      created - created time
      last_modified - last modify time
   """
   user = db.ReferenceProperty(required=True, User, collection_name='posts')
   title = db.StringProperty(required=True)
   content = db.TextProperty(required=True)
   created = db.DateTimeProperty(auto_now_add=True)
   last_modified = db.DateTimeProperty(auto_now=True)


   def render(self):
      '''
      render html for post
      '''
      return 'post~~'


   @classmethod
   def by_id(cls, pid):
      '''
      get post using post_id
      '''
      return cls.get_by_id(int(pid), parent=post_key())


   @classmethod
   def by_user(cls, u):
      '''
      get all posts belong to user
      '''
      return cls.all().filter('user =', u).fetch(limit=None)













