import json
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from time import sleep
import re

class MyListener(StreamListener):

    def on_data(self, data):
        try:
            if (isinterresting(data)):
                pass
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return False

regex_str = [
    r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)

def preprocess(s, lowercase=False):
    tokens = tokens_re.findall(s)
    if lowercase:
        tokens = [token.lower() for token in tokens]
    return tokens

def isinterresting(data):
    data = json.loads(data)
    if data['user']["verified"] == False:
        return False
    tokens = preprocess(data["text"], lowercase=True)
    if (("rt" in tokens or "retweet" in tokens) and "follow" in tokens):
        pass
    else:
        return False
    print("TWEET COOL")
    api.retweet(data["id"])
    api.create_friendship(data['user']['id'])
    with open('giveaways.json', 'a') as f:
        f.write(data)
    sleep(60 * 10)
    return True

keys = json.load(open('auth.json'))

auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
auth.set_access_token(keys['access_token'], keys['access_secret'])

try :
    api = tweepy.API(auth) # create an API object
except :
    print('Error! Failed to get access to twitter API.')

try :
    with open('giveaways.json', 'r') as f:
        lines = f.readlines()
        for line in lines:
            tweet = json.loads(line)
            api.destroy_friendship(tweet['user']['id'])
            try:
                status = next(tweepy.Cursor(api.user_timeline).items(), None)
                api.destroy_status(status['id'])
            except:
                pass
except:
    pass

twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=["giveaway, concours, gifts, cadeaux"])