import sys
# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json


##########################################
#############
############
###########
########## NEHİİİİİİİİİİİİİİİİİİİİİİİİİİİL OKU BURAYI : http://socialmedia-class.org/twittertutorial.html
####################################
############################# import twittertweets
############################# twittertweets.getLastestTweet("iran")  -> kullanımı böyle



# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

import re
import nltk
from regex import RegexReplacer
from nltk.corpus import stopwords
from PorterStemmer import *


def stemm(line):
    p = PorterStemmer()#Here the porter stemmer is initialized.
    line += " "
    line1 = ""
    element = ''
    for c in line:
        if c.isalpha():
            element += c.lower()
        else:
            if element:
                element = p.stem(element, 0,len(element)-1)
                line1 += element
                line1 += " "
                element = ''

    return line1

def getLastestTweet(topic):

    stop = set(stopwords.words('english'))

    rp = RegexReplacer() # Here the replaces is initialized.



    # Variables that contains the user credentials to access Twitter API
    ACCESS_TOKEN = '864949171933073412-AOOaDlBcEFHkwu7rOFx9Te0ukJ7MZPQ'
    ACCESS_SECRET = 'qSdm9nDCc8Eo4OvhJ352rVMkiYLjyB8Gpg1gkYN8oOpvX'
    CONSUMER_KEY = 'WJYjtPc7xzhltoSfdidPjv2ei'
    CONSUMER_SECRET = 'GHj2iwNhT4pNIYXON3YnJTrtGTBEHfqtqq6NYNixDp8r46yZOZ'

    oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

    # Initiate the connection to Twitter Streaming API
    twitter_stream = TwitterStream(auth=oauth)

    # Initiate the connection to Twitter REST API
    twitter = Twitter(auth=oauth)


    # Search for latest tweets about "#given_parameter"
    tweet = twitter.search.tweets(q='#'+topic)
    text = json.dumps(tweet['statuses'][0]['text'])


    #print(text)
    text = text.lower()

    text = rp.replace(text)
    text = re.sub("not ","not_",text)
    filtered_words = ""
    for i in text.split():
        if i not in stop:
            filtered_words+=i
            filtered_words+=" "
        text = stemm(filtered_words)

    #print(text)
    file = open("tweet.txt", "w")
    file.write(text)
    file.close()
