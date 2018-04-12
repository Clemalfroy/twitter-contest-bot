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
    if (data['lang'] != "en") or data['user']["verified"] == False:
        return False
    tokens = preprocess(data["text"], lowercase=True)
    if ("rt" not in tokens or "follow" not in tokens):
        return False
    print(tokens)
    sleep(60)
    return True

keys = json.load(open('auth.json'))

auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
auth.set_access_token(keys['access_token'], keys['access_secret'])

# Construct the API instance
try :
    api = tweepy.API(auth) # create an API object
except :
    print('Error! Failed to get access to twitter API.')

twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=["giveaway"])