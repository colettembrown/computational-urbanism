
# coding: utf-8

# # Scraping Twitter Data
# 
# This code comes from Shadab Hussain (https://github.com/shadab-entrepreneur). 

# In[9]:

# Importing libraries
import json
import tweepy
import pandas as pd
from datetime import date
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import re 
from textblob import TextBlob 


# # Twitter Text Sentiment Analysis: Correlation of neighborhoods in london vs sentiment
# 
# Adapted from : https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/
# 

# In[10]:

class TwitterClient(object): 
    ''' 
    Generic Twitter Class for sentiment analysis. 
    '''
    def __init__(self): 
        ''' 
        Class constructor or initialization method. 
        '''
        # keys and tokens from the Twitter Dev Console 
        consumer_key = 'Ue6lPHym1DacsbQtFPaFdjUgz'
        consumer_secret = 'yO096IxLzAxkEy2sSpZAJZU1F1hV1MP3lo4xeUfrc8ex71MjK5'
        access_token = '1042063897073733632-E9YhTYt11vut5OWUXUPUGujiAZbAcG'
        access_token_secret = 'R3ResgToyI5JV8KViGBXGqzgUappMDlcSFc1uEdwnXqIc'
        
        # attempt authentication 
        try: 
            # create OAuthHandler object 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
            self.auth.set_access_token(access_token, access_token_secret) 
            # create tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed") 
  
    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) 
  
    def get_tweet_sentiment(self, tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method - built on top of NLTK
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
  
    def get_tweets(self, query, max_count = 200): 
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        # empty list to store parsed tweets 
        tweets = [] 
  
        try: 
            # call twitter api to fetch tweets 
            fetched_tweets = self.api.search(q = query, count = max_count) 
  
            # parsing tweets one by one 
            for tweet in fetched_tweets: 
                # empty dictionary to store required params of a tweet 
                parsed_tweet = {} 
  
                # saving text of tweet 
                parsed_tweet['text'] = tweet.text 
                # saving sentiment of tweet 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
  
                # appending parsed tweet to tweets list 
                if tweet.retweet_count > 0: 
                    # if tweet has retweets, ensure that it is appended only once 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
  
            # return parsed tweets 
            return tweets 
  
        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e)) 
  


# In[11]:

# I saved a list of london neighborhoods here
with open('London_Neighborhoods.txt') as inputfile: # try open('...', 'rb') as well
    london_neighborhoods = [line.strip() for line in inputfile]
london_neighborhoods


# In[14]:

from datetime import date
df_total = pd.DataFrame(columns=['sentiment', 'text', 'query'])

def tweets_analysis_per_hashtag(my_query = 'bike', lower_bound = 50, upper_bound = 1000):
    global df_total
    # creating object of TwitterClient Class 
    api = TwitterClient() 
    # calling function to get tweets 
    tweets = api.get_tweets(query = my_query) 
    print("Found {} tweets with query: {}".format(len(tweets), my_query))
    if len(tweets) < lower_bound:
        error_message = "Query {} had only {} tweets, we want at least {}".format(my_query, len(tweets), lower_bound)
        print(error_message)

    # Save as DF
    this_df = pd.DataFrame(tweets)
    this_df['query'] = my_query
    df_total = df_total.append(this_df)
    return df_total

# example
# df_total = tweets_analysis_per_hashtag(my_query = 'shoreditch', lower_bound = 40, upper_bound = 200)


# In[15]:

areas = ['shoreditch','dalston','brixton','peckham','camden','chelsea','clerkenwell','liverpool','Bethnal Green','Clapham','Kensington','City of London','soho']
london_neighborhoods 
for area in areas:
    df_total = tweets_analysis_per_hashtag(my_query = area, lower_bound = 40, upper_bound = 200)

# save to CSV
df_total.to_csv('tweets_{}.csv'.format(str(date.today())))
print("done")


# In[16]:

df_total.groupby(['query','sentiment']).count()


# In[17]:

round(df_total.groupby(['query','sentiment']).count()/df_total[['query','text']].groupby(['query']).count(),2)


# In[19]:

# creating object of TwitterClient Class 
# Example of one neighborhood
api = TwitterClient() 
# calling function to get tweets 
tweets = api.get_tweets(query = 'shoreditch') 

# picking positive tweets from tweets 
ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
# percentage of positive tweets 
print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))) 
# picking negative tweets from tweets 
ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
# percentage of negative tweets 
print("Negative tweets percentage: {}%".format(100*len(ntweets)/len(tweets))) 
# percentage of neutral tweets 
print("Neutral tweets percentage: {}%".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets))) 

# printing first 5 positive tweets 
print("\n\n*Positive tweets*:\n") 
for tweet in ptweets[:10]: 
    print(tweet['text']) 

# printing first 5 negative tweets 
print("\n\n*Negative tweets*:\n") 
for tweet in ntweets[:10]: 
    print(tweet['text']) 


# In[ ]:



