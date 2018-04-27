import re
from time import sleep
import datetime
from random import randint


def tokenizeTweet(str, lowercase=False):
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
    tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
    tokens = tokens_re.findall(str)
    if lowercase:
        tokens = [token.lower() for token in tokens]
    return tokens

def processTweet(status, API):
    if hasattr(status, 'retweeted_status'):
        status = status.retweeted_status

    if not status.user.verified or (datetime.datetime.now() - status.created_at).days > 1:
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
                API.update_status('@Quilyo', status.id)

            API.retweet(status.id)
            API.create_friendship(status.user.screen_name, follow=True)
            for token in tokens:
                if token[0] == "@":
                    API.create_friendship(token, follow=True)
            print(tweet + "\n\n\n----------------------------------\n\n\n")
            sleep(randint(0, 300))

        except:
            pass
