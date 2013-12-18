import json
from requests_oauthlib import OAuth1Session
from dogefortune import dogeconfig

# Set up Twitter access
t = OAuth1Session(dogeconfig.TWITTER_CONSUMER_KEY,
                  dogeconfig.TWITTER_CONSUMER_SECRET,
                  dogeconfig.TWITTER_OAUTH_TOKEN,
                  dogeconfig.TWITTER_OAUTH_SECRET)


def send_dm(user, text):
    url = "https://api.twitter.com/1.1/direct_messages/new.json"
    data = {"screen_name": user, "text": text}
    return t.post(url, data=data)


def send_tweet(tweet):
    url = "https://api.twitter.com/1.1/statuses/update.json"
    data = {"status": tweet}
    return t.post(url, data=data)


def stream_followers():
    url = "https://userstream.twitter.com/1.1/user.json"
    r = t.get(url, stream=True)
    me = dogeconfig.TWITTER_USERNAME
    for line in r.iter_lines(chunk_size=8):
        if line:
            msg = json.loads(line.decode('utf-8'))
            if 'event' in msg and msg['event'] == 'follow':
                if 'target' in msg and msg['target']['screen_name'] == me:
                    yield msg['source']['screen_name']
