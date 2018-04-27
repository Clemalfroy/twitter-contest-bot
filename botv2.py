import tweepy
from json import load
from StreamListener import Stream

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