import time
import json
import requests

from multiprocessing import Process
from requests_oauthlib import OAuth1Session
from dogefortune import dogeconfig

# Set up Twitter access
t = OAuth1Session(dogeconfig.TWITTER_CONSUMER_KEY,
                  dogeconfig.TWITTER_CONSUMER_SECRET,
                  dogeconfig.TWITTER_OAUTH_TOKEN,
                  dogeconfig.TWITTER_OAUTH_SECRET)

# Set up dogecoin access
rpcauth = (dogeconfig.DOGECOIN_RPC_USER, dogeconfig.DOGECOIN_RPC_PASS)
rpcurl = dogeconfig.DOGECOIN_RPC_URL

# Globals r cool
last_block_hash = "0"
try:
    with open("last_block_hash", "r") as f:
        last_block_hash = f.read()
except IOError:
    pass


def dogerpc(method, args=None):
    if not args:
        args = []
    headers = {"Content-Type": "application/json"}
    payload = {"jsonrpc": "1.0", "id": "dogefortune",
               "method": method, "params": args}
    data = json.dumps(payload)
    req = requests.get(rpcurl, auth=rpcauth, headers=headers, data=data).json()
    return req['result']


def get_transactions():
    global last_block_hash
    r = dogerpc("listsinceblock", [last_block_hash])
    last_block_hash = r['lastblock']
    try:
        with open("last_block_hash", "w") as f:
            f.write(last_block_hash)
    except IOError:
        pass
    return r['transactions']


def get_address(username):
    return dogerpc("getaccountaddress", [username])


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


def twitter_loop():
    for follower in stream_followers():
        address = get_address(follower)
        print("Followed by {0}, address {1}".format(follower, address))
        msg = "much follow, very donate, so fortune: {0}"
        send_dm(follower, msg.format(address))


def dogecoin_loop():
    while True:
        for tx in get_transactions():
            account = tx["account"]
            amount = tx["amount"]
            print("Received {0}DOGE from {1}".format(amount, account))
            msg = "@{0} very thanks, much generous {1} doges"
            send_tweet(msg.format(account, amount))
        time.sleep(30)


def main():
    twitter_proc = Process(target=twitter_loop)
    dogecoin_proc = Process(target=dogecoin_loop)
    twitter_proc.start()
    dogecoin_proc.start()
    try:
        twitter_proc.join()
        dogecoin_proc.join()
    except KeyboardInterrupt:
        print("Terminating children...")
        twitter_proc.terminate()
        dogecoin_proc.terminate()

if __name__ == "__main__":
    main()
