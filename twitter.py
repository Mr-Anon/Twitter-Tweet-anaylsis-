# import pandas as pd
# from pandas import DataFrame
# import pymongo
# from pymongo import MongoClient
# import json
# import tweepy as tw
# from pprint import pprint

# API_KEY = "qU3xA0HXN6G0l6rZlsTI9G2Ba"
# API_SECRET_KEY = "KZsAAMWuZrfULqcq5OePEMig0v7RzdFIqd9I3ieMwqnOMRqXDw"

# auth = tw.OAuthHandler(API_KEY, API_SECRET_KEY)
# api = tw.API(auth, wait_on_rate_limit=False)

# # client = MongoClient()
# # db = client.tweet_db
# # tweets = db.tweets
# # tweets.create_index([("id", pymongo.ASCENDING)], unique=True)

# count = 10

# search_query = "#INDvsAUSTest -filter:retweets"


# result = tw.Cursor(api.search,
#                    q=search_query,
#                    lang="en",
#                    since="2000-01-01").items(count)

# # store the API responses in a list
# tweets_copy = []
# for tweet in result:
#     # try:
#     #     tweets.insert_many(tweet)
#     # except:
#     #     print("error")
#     # pass

#     tweets_copy.append(tweet)


# print("Total Tweets fetched:", len(tweets_copy))

# # intialize the dataframe
# tweets_df = pd.DataFrame()

# # populate the dataframe
# for tweet in tweets_copy:
#     hashtags = []
#     try:
#         for hashtag in tweet.entities["hashtags"]:
#             hashtags.append(hashtag["text"])
#         text = api.get_status(id=tweet.id, tweet_mode='extended').full_text
#     except:
#         pass
#     tweets_df = tweets_df.append(pd.DataFrame({'user_name': tweet.user.name,
#                                                'user_location': tweet.user.location,
#                                                'user_description': tweet.user.description,
#                                                'user_verified': tweet.user.verified,
#                                                'date': tweet.created_at,
#                                                'text': text,
#                                                'hashtags': [hashtags if hashtags else None],
#                                                'source': tweet.source}))
#     tweets_df = tweets_df.reset_index(drop=True)

# # show the dataframe

import pandas as pd
import matplotlib
from pandas import DataFrame
import json
import excel
import tweepy as tw


API_KEY = "xloKoOYLYwftMGE1JcBaJ0csx"
API_SECRET_KEY = "xG4MdEYo5W6SGhTRb0SYGYvGE5gzHbckbuwenIO6kN6xPORZ68"
ACCESS_TOKEN = "1340243550898774016-7am491fPZXjo0M0gzl7OVOhFlmOyw5"
ACCESS_TOKEN_SECRET = "dC74oCfNJQwvcgn5YyfyVLHAQsA1mudbQue17hezhYz3A"

auth = tw.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tw.API(auth, wait_on_rate_limit=True)


count = 10000

search_query = "#INDvsAUSTest -filter:retweets"


result = tw.Cursor(api.search,
                   q=search_query,
                   since="2000-01-01").items(count)

print("starting")
tweets_copy = []
tweets_df = pd.DataFrame()
for tweet in result:
    hashtags = []

    try:
        for hashtag in tweet.entities["hashtags"]:
            hashtags.append(hashtag["text"])
        text = api.get_status(id=tweet.id, tweet_mode='extended').full_text
    except:
        pass
    tweets_df = tweets_df.append(pd.DataFrame({'user_name': tweet.user.name,
                                               'user_location': tweet.user.location,
                                               'user_description': tweet.user.description,
                                               'user_verified': tweet.user.verified,
                                               'date': tweet.created_at,
                                               'text': text,
                                               'retweet_count': tweet.retweet_count,
                                               'followers_count': tweet.user.followers_count,
                                               'len': len(text),
                                               'lang': tweet.lang,
                                               'hashtags': [hashtags if hashtags else None],
                                               'source': tweet.source}))
    tweets_df = tweets_df.reset_index(drop=True)

# show the dataframe
print("done")

with open('dump.json', 'w') as json_file:
    json.dump(tweets_df.to_json(orient="table"), json_file)

tweets_df.to_excel("output.xlsx",
                   sheet_name='Sheet_name_1')
