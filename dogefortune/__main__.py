import time
from multiprocessing import Process
from dogefortune import twitter, dogecoin, fortune


def twitter_loop():
    for follower in twitter.stream_followers():
        address = dogecoin.get_address("@" + follower)
        print("Followed by {0}, address {1}".format(follower, address))
        msg = "much follow, very donate, so fortune: {0}"
        twitter.send_dm(follower, msg.format(address))


def dogecoin_loop():
    while True:
        for tx in dogecoin.get_transactions():
            account = tx["account"]
            amount = tx["amount"]
            if amount < 0 or not account or account[0] != "@":
                continue
            print("Received {0}DOGE from {1}".format(amount, account))
            msg = (account + " " + fortune.get_fortune())[:140]
            twitter.send_tweet(msg.format(account, amount))
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
