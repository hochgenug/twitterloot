import tweepy
from secrets import *
import re

filepath = 'listTweetID.txt'
listTweetID = []
try:
    with open(filepath) as fp:
        for cnt, line in enumerate(fp):
           listTweetID.append(int(line))
finally:
    fp.close()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth,wait_on_rate_limit=True)

f = open(filepath, "a+")
regex = r"(^|[^@\w])@(\w{1,15})\b"

for tweet in tweepy.Cursor(api.search,q="concours RT",
                           lang="fr",result_type='popular').items(40):

    print("\n===============================================")
    print("Tweet ID : ", int(tweet.id_str))
    if int(tweet.id_str) in listTweetID:
        print("already here")
        continue

    else:
        print (tweet.text)
        matches = re.findall(regex, tweet.text)
        for match in matches:
            print("Follow @%s" % (match[1]))
            #print(tweet.id)
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

            f.write(str(int(tweet.id_str)) + "\n")
f.close()