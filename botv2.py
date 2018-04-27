import tweepy

from json import load
from random import randint
from time import sleep
from handler.tweet_handler import processTweet

class Stream(tweepy.StreamListener):
    def on_connect(self):
        print("Succesfully connected\n")

    def on_status(self, status):
        processTweet(status, self.api)

    def on_exception(self, exception):
        print(exception)
        sleep(randint(0, 300))

    def on_error(self, status_code):
        if status_code == 420:
            print("Limit rate reached")
            sleep(601)
            return False

def connect():
    try:
        keys = load(open('auth.json'))
        auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
        auth.set_access_token(keys['access_token'], keys['access_secret'])
        return tweepy.API(auth)
    except :
        return False

def launchStream(API):
    try:
        streamListener = Stream(API)
        myStream = tweepy.Stream(auth=API.auth, listener=streamListener)
        myStream.filter(track=["giveaway, concours, gifts, cadeaux, cadeau, gift"])
    except:
        launchStream(API)

def main():
    API = connect()
    if not API:
        print("Connection with API failed.")
        exit(1)
    launchStream(API)

if __name__  == "__main__":
    main()