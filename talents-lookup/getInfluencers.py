
# coding: utf-8

# In[56]:

import pandas as pd
import json, re
import collections
from textblob import TextBlob
from operator import itemgetter

with open('tweetsN.json') as json_data:
    d = json.load(json_data)

def clean_tweet(tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def get_tweet_sentiment(tweet):
    '''
    Utility function to classify sentiment of passed tweet
    using textblob's sentiment method
    '''
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    return analysis.sentiment.polarity
    # set sentiment
#     if analysis.sentiment.polarity > 0:
#         return 'positive'
#     elif analysis.sentiment.polarity == 0:
#         return 'neutral'
#     else:
#         return 'negative'

userlist = []
f = {}
tw = {}
l = {}
for each in d:
    mentions = []
    tweet = each['text']
#     time.append(each['created_at'])
    screen_name = each['user']['screen_name']
    followers = each['user']['followers_count']
    location = each['user']['location']
    sentiment = get_tweet_sentiment(each['text'])
    mentions.append(screen_name)
    mentions.append(followers)
    mentions.append(sentiment)
#     mentions.append(location)
#     mentions.append(tweet)
#     statuses_count = each['user']['statuses_count']
#     friends = each['user']['friends_count']  
    userlist.append(mentions)
    f[screen_name] = followers
    l[screen_name] = location

#     if screen_name in tw.keys():
#         tw[screen_name].append(tweet)
#     else:
#         tw[screen_name] = [tweet]

pivot = collections.defaultdict(list)

for item in userlist:
    pivot[item[0]].append(item[2])
l = [{'Nickname':k, 'Sentiment':sum(values)/len(values), '# of mentions':len(values), '# of followers': f[k], 'Rating': sum(values)/len(values) + len(values) + f[k]/100000, 'Location': l[k]} for k, values in pivot.items()]
# with the text of tweets
# l = [{'nickname':k, 'sentiment':sum(values)/len(values), 'mentions':len(values), 'followers': f[k], 'rating': sum(values)/len(values) + len(values) + f[k]/100000, 'tweets': ' '.join(el for el in tw[k])} for k, values in pivot.items()]
df = pd.DataFrame(l)
pd.options.display.max_colwidth = 10000
s = df.sort_values(by='Rating', ascending=[False]) 
s = s[['Nickname', '# of mentions', '# of followers', 'Sentiment', 'Rating', 'Location']]
print (s.head(n =20))

filename = 'results.csv'
s.to_csv(filename, index=True, encoding='utf-8')


