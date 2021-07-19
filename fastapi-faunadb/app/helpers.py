import os
import random
import pytz
import time
from bson import ObjectId
from pathlib import Path
from datetime import datetime
from decouple import config
from faunadb import query as q
from faunadb.client import FaunaClient 
from faunadb.objects import Ref 
from faunadb.errors import BadRequest, NotFound
from faker import Faker
from models import TweetCategoryEnum

tweetCategories = [e.value for e in TweetCategoryEnum]

fake = Faker()

# Initialize the FaunaDB client
FAUNA_SECRET_KEY = config('FAUNA_SECRET_KEY')
client = FaunaClient(secret=FAUNA_SECRET_KEY)
indexes = client.query(q.paginate(q.indexes()))

# Show FaunaDB indexes
# print(indexes)

class User:
    """
        Description:- Helper functions for User model (CRUD)
    """
    def __init__(self):
        self.collection = 'users'

    def register_user(self, data : dict):
        """ CREATE - Register a new user """
        new_user = client.query(
            q.create(
                q.collection(self.collection),
                {'data' : {
                    **data,
                    'following':0,
                    'followers':0,
                    'id' : str(ObjectId())
                }}
            )
        )

        return new_user['data']
    
    def update_user(self, data : dict, user_id : str):
        """ UPDATE - Update a user's profile details. """
        try:
            id = self.get_user(user_id)['ref'].id()
            updated_user = client.query(
                q.update(
                    q.ref(q.collection(self.collection), id),
                    {'data' : data}
                )
            )
        except (Exception,NotFound) as e:
            print(e)
            return None

        return updated_user['data']

    def delete_user(self, user_id : str):
        """ DELETE - Delete a user from the users collection. """
        try:
            id = self.get_user(user_id)['ref'].id()
            deleted_user = client.query(
                q.delete(
                    q.ref(q.collection(self.collection), id)
                )
            )
        except (Exception,NotFound) as e:
            print(e)
            return None 
        
        return deleted_user['data']

    def get_all_users(self):
        """ Get all the users in the users collection """
        try:
            # Using the "all_users" index defined in FaunaDB indexes for the database
            users = client.query(
                q.paginate(q.match(q.index('all_users')))
            )
        except NotFound as e:
            return None 
        
        if users.get('errors'):
            return None
        else:
            # Get the data for each user Fauna ID returned.
            return list(map(lambda user: client.query(q.get(q.ref(q.collection('users'), user.id())))['data'], users['data']))

    def get_user(self, user_id : ObjectId()):
        """ Fetch a user based on user ID. """
        try:
            # Using the "user_by_id" index
            user = client.query(
                q.get(q.match(q.index('user_by_id'), user_id))
            )

        except NotFound as e:
            print(e)
            return None 
        
        return None if user.get('errors') else user

    def get_user_by_email(self, email : str):
        """ Fetch a user based on user email. """
        try:
            # Using the "user_by_email" index
            user = client.query(
                q.get(q.match(q.index('user_by_email'),email))
            )

        except NotFound as e:
            return None
        return None if user.get('errors') else user['data']

    def get_user_by_username(self, username : str):
        """ Fetch a user based on username """
        try:
            # Using the "user_by_username" index
            user = client.query(
                q.get(q.match(q.index('user_by_username'),username))
            )

        except NotFound as e:
            return None
        
        return None if user.get('errors') else user['data']

class Tweet:
    """
        Description:- Helper functions for Tweet model (CRUD)
    """
    def __init__(self):
        self.collection = 'tweets'
    
    def create_tweet(self, data : dict, user_id : str):
        """ CREATE - Add a new tweet for a user. """
        new_tweet = client.query(
            q.create(
                q.collection(self.collection),
                {'data' : {**data, 'id' : str(ObjectId()), 'user_id' : user_id}}
            )
        )

        return new_tweet['data']

    def get_tweet(self, tweet_id: ObjectId()):
        """ Fetch tweet based on the tweet_id """
        try:
            # Using the "tweet_by_id" index
            tweet = client.query(
                q.get(q.match(q.index('tweet_by_id'), tweet_id))
            )
        except (Exception,NotFound) as e:
            return None 
        
        return None if tweet.get('errors') else tweet

    def get_all_tweets(self):
        """ Fetch all tweets in the tweets collection """
        try:
            # Using the "all_tweets" index
            tweets = client.query(
                q.paginate(q.match(q.index('all_tweets')))
            )
        except (Exception,NotFound) as e:
            return None 

        if tweets.get('errors'):
            return None
        else:
            return list(map(lambda tweet: client.query(q.get(q.ref(q.collection(self.collection), tweet.id())))['data'], tweets['data']))

    def get_all_user_tweets(self,user_id : str):
        """ Fetch all tweets for a specific user """
        try:
            # Using the "tweets_by_user" index
            user_tweets = client.query(
                q.paginate(q.match(q.index('tweets_by_user'), user_id))
            )
            print(user_tweets)
        except (Exception,NotFound) as e:
            return None 

        if user_tweets.get('errors'):
            return None 
        else:
            # Returns tweet documents for the user
            return list(map(lambda tweet: client.query(q.get(q.ref(q.collection(self.collection), tweet.id())))['data'], user_tweets['data']))


    def update_tweet(self, data : dict, tweet_id):
        """ UPDATE - Update tweet based on tweet_id """
        try:
            id = self.get_tweet(tweet_id)['ref'].id()
            updated_tweet = client.query(
                q.update(
                    q.ref(q.collection(self.collection), id),
                    {'data': data}
                )
            )
        except (Exception, NotFound) as e:
            return None 
        
        return updated_tweet['data']

    def delete_tweet(self, tweet_id : str):
        """ DELETE - Delete tweet based on tweet_id """
        try:
            id = self.get_tweet(tweet_id)['ref'].id()
            deleted_tweet = client.query(
                q.delete(
                    q.ref(q.collection(self.collection), id)
                )
            )
        except (Exception,NotFound) as e:
            return None

        return deleted_tweet['data']

class Comment:
    """
        Description:- Helper functions for Comment model.
    """
    def __init__(self):
        self.collection = 'comments'

    def add_comment(self, data, tweet_id : str, user_id : str):
        """ Add a new comment """
        new_comment = client.query(
            q.create(
                q.collection(self.collection),
                {'data': {**data, 'id': str(ObjectId()), 'tweet_id': tweet_id, 'user_id': user_id}}
            )
        )

        return new_comment['data']

    def get_all_comments_tweet(self, tweet_id : str):
        """ Fetch all the comments for a particular tweet """
        try:
            # Using the "tweets_by_user" index
            tweet_comments = client.query(
                q.paginate(q.match(q.index('comments_by_tweet'), tweet_id))
            )
            print(tweet_comments)
        except (Exception,NotFound) as e:
            return None 

        if tweet_comments.get('errors'):
            return None 
        else:
            # Returns tweet documents for the user
            return list(map(lambda comment: client.query(q.get(q.ref(q.collection(self.collection), comment.id())))['data'], tweet_comments['data']))

    def delete_comment(self, comment_id : str):
        """ DELETE - Delete a comment """
        try:
            deleted_comment = client.query(
                q.delete(
                    q.ref(q.collection(self.collection), comment_id)
                )
            )
        except (Exception,NotFound) as e:
            return None 

        return deleted_comment['data']

class Relationship:
    """
        Description:- Helper functions for Relationship model (i.e. follow/unfollow)
    """
    def __init__(self):
        self.collection = 'relationships'

    def follow(self, follower_user_id : ObjectId(), following_user_id : ObjectId()):
        """ Follow a user """
        following_user = User().get_user(following_user_id)
        follower_user = User().get_user(follower_user_id)
        if not following_user or not follower_user:
            return None 
            
        data = {
            'follower_id' : follower_user_id,
            'following_id' : following_user_id,
            'created_at' : datetime.now(pytz.UTC)
        }
        new_relationship = client.query(
            q.create(
                q.collection(self.collection),
                {'data' : {**data , 'id' : str(ObjectId())}}
            )
        )

        return new_relationship['data']

        
    def get_user_followers(self, user_id : str):
        """ Fetch all users following a specific user """
        try:
            user_followers = client.query(
                q.paginate(q.match(q.index('get_user_followers'), user_id))
            )
            print(user_followers['data'])
        except (Exception, NotFound) as e:
            return str(e) or None

        followers_id = list(map(
            lambda relationship: client.query(q.get(q.ref(q.collection(self.collection), relationship.id())))['data']['follower_id'],
            user_followers['data']
        ))
        user_followers = list(map(lambda user_id: User().get_user(user_id)['data'], followers_id))
        return user_followers 

    def get_user_following(self, user_id : str):
        """ Get all users being followed by a specific user """
        try:
            user_following = client.query(
                q.paginate(q.match(q.index('get_user_following'), user_id))
            )
        except (Exception, NotFound) as e:
            return str(e) or None

        following_ids = list(map(
            lambda relationship: client.query(q.get(q.ref(q.collection(self.collection), relationship.id())))['data']['following_id'],
            user_following['data']
        ))
        user_following = list(map(lambda user_id: User().get_user(user_id)['data'], following_ids))
        return user_following

if __name__ == '__main__':
    
    fakeName = fake.name()

    new_user = {
        'fullname' : fakeName,
        'username' : "-".join(fakeName.split(" ")).lower(),
        'email' : fake.email(),
        'password' : 'adetoyosi',
        'status' : fake.text()[:300],
        'website' : fake.url(),
        'created_at' : datetime.now(pytz.UTC),
        'updated_at' : datetime.now(pytz.UTC)
    }

    new_tweet = {
        'tweet' : fake.text(),
        'category' : random.choice(tweetCategories),
        'tags' : [random.choice(tweetCategories) for i in range(2)],
        'created_at' : datetime.now(pytz.UTC),
        'updated_at' : datetime.now(pytz.UTC)
    }

    userModel = User()
    tweetModel = Tweet()
    commentModel = Comment()
    relationshipModel = Relationship()

    start = time.time()
    # print(userModel.register_user(new_user))
    print(userModel.get_all_users())
    # print(userModel.get_user('6059bf808b42f324cc07e149'))
    # print(userModel.get_user_by_username('sopeokunowo'))
    # print(userModel.delete_user('60399baf8b42f336482dd8cd'))
    # print(tweetModel.get_all_tweets())
    # print(tweetModel.create_tweet(new_tweet,'6031951a8b42f33db4ac1c5a'))
    # print(tweetModel.get_all_user_tweets('603194358b42f33e50272d0f'))
    # print(tweetModel.get_tweet('603195688b42f3025cced026')['data'])
    # print(tweetModel.update_tweet({'tweet':fake.text()}, 291088261247402498))
    # print(relationshipModel.follow('603194c48b42f33db0e207bf','603194868b42f33a2816aae0'))
    # print(relatioonshipModel.get_user_followers('603194358b42f33e50272d0f'))
    # print(relationshipModel.get_user_following('603194868b42f33a2816aae0'))
    # print(commentModel.add_comment({'message':fake.text()}, '603195688b42f3025cced026', '60399baf8b42f336482dd8cd'))
    # print(commentModel.get_all_comments_tweet('603195688b42f3025cced026'))
    end = time.time()
    print(f"Time elapsed :- {end-start}s")

