from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.sentiment.util import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def word_filter(twts):
    tkn = TweetTokenizer()
    tweets = []
    for t in twts:
        t = tkn.tokenize(t)
        print(t)
        t = [word for word in t if word not in stopwords.words('english')]
        tweets.append(t)
    return tweets


def get_sentiment(sentence):
    sid = SentimentIntensityAnalyzer()
    s = sid.polarity_scores(sentence)
    return s


def avg_sentiment(tweets):
    avg = {'neg': 0, 'neu': 0, 'pos': 0, 'compound': 0}
    for tweet in tweets:
        avg['neg'] += get_sentiment(tweet)['neg']
        avg['neu'] += get_sentiment(tweet)['neu']
        avg['pos'] += get_sentiment(tweet)['pos']
        avg['compound'] += get_sentiment(tweet)['compound']

    avg['neg'] = avg['neg'] / len(tweets)
    avg['neu'] = avg['neu'] / len(tweets)
    avg['pos'] = avg['pos'] / len(tweets)
    avg['compound'] = avg['compound'] / len(tweets)
    return avg
