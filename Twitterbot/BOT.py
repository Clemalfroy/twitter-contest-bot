import json
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener

keys = dbinfo = json.load(open('auth.json'))

# create an OAuthHandler instance
# Twitter requires all requests to use OAuth for authentication
auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])

auth.set_access_token(keys['access_token'], keys['access_secret'])

# Construct the API instance
try :
    api = tweepy.API(auth) # create an API object
except :
    print('Error! Failed to get access to twitter API.')

# print (api.rate_limit_status())

# Iterate through all of the authenticated user's friends
# for friendinfo in tweepy.Cursor(api.friends).items():
#     print (friendinfo)

# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#         print(tweet.text)

user = api.get_user('Daggerron1')
print(user)
print(user.screen_name)
print(user.followers_count)
for friend in user.friends():
    print(friend.screen_name)

class MyListener(StreamListener):

    def on_data(self, data):
        try:
            with open('python.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return False


twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(follow=["321388777"]) #gotaga id