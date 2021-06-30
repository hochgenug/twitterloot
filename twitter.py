import os
import tweepy
import re
from secrets import *
from dotenv import load_dotenv

load_dotenv()
filepath = 'listTweetID.txt'
listTweetID = []
try:
    with open(filepath) as fp:
        for cnt, line in enumerate(fp):
            listTweetID.append(int(line))
    fp.close()
except FileNotFoundError:
    f = open("listTweetID.txt", "w")

auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_SECRET'))

api = tweepy.API(auth,wait_on_rate_limit=True)

f = open(filepath, "a+")
regex = r"(^|[^@\w])@(\w{1,30})"

for tweet in tweepy.Cursor(api.search,q="concours RT",
                           lang="fr",result_type='popular', tweet_mode='extended').items(int(os.getenv('SEARCH_ITEM_NUMBER'))):

    if int(tweet.id_str) in listTweetID:
        if os.getenv('DEBUG') == 1:
            print("tweet already processed : ",int(tweet.id_str))
        continue

    else:
        print("\n===============================================")
        print("Tweet ID : ", int(tweet.id_str))
        print (tweet.full_text)
        f.write(str(int(tweet.id_str)) + "\n")
        matches = re.findall(regex, tweet.full_text)
        for match in matches:
            print("Follow @%s" % (match[1]))
            try:
                api.create_friendship(match[1])
            except Exception as e:
                print(e)
                pass

        try:
            api.create_favorite(tweet.id)
        except Exception as e:
            print(e)
            pass

        try:
            tweet.retweet()
        except Exception as e:
            print(e)
            pass

f.close()