import os
import tweepy
import re
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
newtweetcounter, oldtweetcounter, ignorecounter = 0, 0, 0

for tweet in tweepy.Cursor(api.search, q="concours RT",
                           lang="fr", result_type='popular', count=int(os.getenv('SEARCH_ITEM_NUMBER')),
                           tweet_mode='extended').items(int(os.getenv('SEARCH_ITEM_NUMBER'))):

    if int(tweet.id_str) in listTweetID:
        if int(os.getenv('DEBUG')) == 1:
            print("tweet already processed : ",int(tweet.id_str))
        oldtweetcounter += 1
        continue
    elif (tweet.in_reply_to_status_id is not None) or hasattr(tweet, 'retweeted_status'):
        if int(os.getenv('DEBUG')) == 1:
            print("tweet is a reply/RT : ",int(tweet.id_str))
        ignorecounter += 1
        continue

    else:
        print("\n===============================================")
        print("Tweet ID : ", int(tweet.id_str))
        print (tweet.full_text)
        f.write(str(int(tweet.id_str)) + "\n")
        matches = re.findall(regex, tweet.full_text)
        newtweetcounter += 1
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
            api.create_friendship(tweet.user.screen_name)
        except Exception as e:
            print(e)
            pass

        try:
            tweet.retweet()
        except Exception as e:
            print(e)
            pass

print('Subscribed to',newtweetcounter,'new contests.',oldtweetcounter,'were ignored (already subscribed)',ignorecounter,'were ignored (reply or RT)')
f.close()