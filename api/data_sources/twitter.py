# https://github.com/ideoforms/python-twitter-examples/blob/master/twitter-user-search.py

from twitter import *
from private import TWITTER_KEYS


def get_twitter_users(input):

    twitter = Twitter(auth=OAuth(TWITTER_KEYS['access_key'],
                      TWITTER_KEYS['access_secret'],
                      TWITTER_KEYS['consumer_key'],
                      TWITTER_KEYS['consumer_secret']))

    results = twitter.users.search(q=input, count=20)

    output = {'num_users': len(results),
              'users': []}
    for user in results[:5]:
        user_data = {}
        user_data['screen_name'] = user['screen_name']
        user_data['followers_count'] = user['followers_count']
        user_data['friends_count'] = user['friends_count']
        user_data['favourites_count'] = user['favourites_count']
        output['users'].append(user_data)

    return output

