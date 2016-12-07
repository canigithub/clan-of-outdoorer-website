from google.appengine.ext import db

from flask import render_template

from user_model import User
from post_model import Post


##### #####

def comment_key(name='default'):
   '''
   ensure hierarchy for future use.
   default parent key: Key('comment', 'default')
   '''
   return db.Key.from_path('comment', name)



##### Model - Comment

class Comment(db.Model):
   '''
   Model - Comment:
      user - foreign key to User
      post - foreign key to Post
      content - comment content
      created - created time
      last_modified - last modify time
   '''
   user = db.ReferenceProperty(required=True, User, collection_name='comments')
   post = db.ReferenceProperty(required=True, Post, collection_name='comments')
   content = db.TextProperty(required=True)
   created = db.DateTimeProperty(auto_now_add=True)
   last_modified = db.DateTimeProperty(auto_now=True)


   def render(self):
      '''
      render html for comment
      '''
      return 'comment-.-'


   @classmethod
   def by_post(cls, p):
      '''
      fetch all comments belong to post
      '''
      return cls.all().filter('post =', p)..order('-created').fetch(limit=None)


   @classmethod
   def add_comment(cls, u, p, c):
      '''
      user add new comment to post
      '''
      comment = cls(parent=comment_key, user=u, post=p, content=c)
























