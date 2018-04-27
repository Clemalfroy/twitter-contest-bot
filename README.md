# twitter-contest-bot

## What is it ?

* This is a bot, that finds every recent contest on twitter and RT, follow and favorite if needed the tweet in order to win.
* I've won at leat one contest/giveaway per day so far.

## Dependencies:

* Python 3
* Tweepy

## How to run it:

Find your credentials on : [twitter-apps](https://apps.twitter.com/)

Create a file called 'auth.json' that looks like that:
```
{
  "consumer_key" : "XXXXXXXXX",
  "consumer_secret" : "XXXXXXXX",
  "access_token" : "XXXXXXXXX",
  "access_secret" : "XXXXXXXX"
}
```

Then run:

```
python3 bot.py
```
