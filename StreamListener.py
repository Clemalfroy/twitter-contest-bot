import tweepy
import re
from time import sleep
from random import randint

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

def tokenizeTweet(str, lowercase=False):

    tokens = tokens_re.findall(str)
    if lowercase:
        tokens = [token.lower() for token in tokens]
    return tokens

def processTweet(status, API):
    if hasattr(status, 'retweeted_status'):
        status = status.retweeted_status

    if not status.user.verified:
        return

    try:
        tweet = status.extended_tweet["full_text"]
    except AttributeError:
        tweet = status.text

    tokens = tokenizeTweet(tweet, lowercase=True)

    if ("rt" in tokens or "retweet" in tokens) and "follow" in tokens:
        try:

            if "favorite" in tokens or "fav" in tokens or "like" in tokens:
                API.create_favorite(status.id)
            if "tag" in tokens:
                API.update_status('@Daggerron1', status.id)

            API.retweet(status.id)
            API.create_friendship(status.user.screen_name, follow=True)
            for token in tokens:
                if token[0] == "@":
                    API.create_friendship(token, follow=True)
            print(tweet)
            print("\n\n\n----------------------------------\n\n\n")
            sleep(randint(0, 300))

        except:
            pass

class Stream(tweepy.StreamListener):

    def on_connect(self):
        print("Succesfully connected\n")

    def on_status(self, status):
        processTweet(status, self.api)


    def on_error(self, status_code):
        if status_code == 420:
            print("Limit rate reached")
            sleep(601)
            return False

    def on_exception(self, exception):
        print(exception)
        sleep(randint(0, 300))
