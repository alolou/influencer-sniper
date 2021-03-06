import tweepy
import sys
import jsonpickle
import os

API_KEY    = 'v2sK8SKbCTzrPhUkxYKEB8luX'
API_SECRET = '2WiEZ5ExP4KFLzUmPxlKifEyPiouISPO5sbqyEddQEHTd8JG8z'

auth = tweepy.AppAuthHandler(API_KEY, API_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True,
                   wait_on_rate_limit_notify=True)

if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)

searchQuery = '@jet -jetblue OR #shoppurple OR #jetcom OR #purplebox'
maxTweets = 20000
tweetsPerQry = 100
fName = 'tweets.json'
sinceId = None
max_id = -1
i = 0
tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))

all_tweets = []

while tweetCount < maxTweets:
    try:
        if (max_id <= 0):
            if (not sinceId):
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
            else:
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                        since_id=sinceId)
            
        else:
            if (not sinceId):
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                        max_id=str(max_id - 1))
            else:
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                        max_id=str(max_id - 1),
                                        since_id=sinceId)
        if not new_tweets:
            print("No more tweets found")
            break

        for t in new_tweets:
            all_tweets.append(jsonpickle.encode(t._json, unpicklable=False))

        tweetCount += len(new_tweets)

        print("Downloaded {0} tweets".format(tweetCount))
        max_id = new_tweets[-1].id
    except tweepy.TweepError as e:
        print("some error : " + str(e))
        break


with open('tweetsN.json', 'w') as f:
    f.write('[' + '\n')
    f.write(",\n".join(all_tweets))
    f.write(']')
    f.close()
    

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))