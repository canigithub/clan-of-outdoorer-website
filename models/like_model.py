from google.appengine.ext import db

from user_model import User
from post_model import Post


##### #####

def like_key(name='default'):
   '''
   ensure hierarchy for future use.
   default parent key: Key('likes', 'default')
   '''
   return db.Key.from_path('likes', name)



##### Model - Like

class Like(db.Model):
   '''
   Model - Like:
      user - foreign key to User
      post - foreign key to Post
   '''
   user = db.ReferenceProperty(required=True, User, collection_name='likes')
   post = db.ReferenceProperty(required=True, Post, collection_name='likes')


   @classmethod
   def by_user_post(cls, u, p):
      '''
      get Like instance given user and post
      '''
      return cls.all().filter('user =', u).filter('post =', p).get()


   @classmethod
   def get_num_likes(cls, p):
      '''
      fetch the number of likes of a post
      '''
      return cls.all().filter('post =', p).count()


   @classmethod
   def add_like(cls, u, p):
      '''
      user add like to post
      '''
      like = cls(parent=like_key(), user=u, post=p)
      like.put()










