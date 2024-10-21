import requests
import nltk
import os
import json
import numpy as np
import pandas as pd
import nltk
import matplotlib
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from string import punctuation
import re
import numpy as np
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from rake_nltk import Rake
from datetime import datetime,timedelta
date=datetime.now()-timedelta(1)
date=date.strftime('%Y-%m-%d')

url = 'https://newsapi.org/v2/everything?'
api_key = '9cc1b62d32e547bbbb09938de1601768'

# function to take raw data from the API and process it into a list inorder to trnasform it into a pandas dataframe
def get_articles(file):
    article_results = []
    for i in range(len(file)):
        article_dict = {}
        article_dict['title'] = file[i]['title']
        article_dict['author'] = file[i]['author']
        article_dict['source'] = file[i]['source']
        article_dict['description'] = file[i]['description']
        article_dict['content'] = file[i]['content']
        article_dict['pub_date'] = file[i]['publishedAt']
        article_dict['url'] = file[i]["url"]
        article_dict['photo_url'] = file[i]['urlToImage']
        article_results.append(article_dict)
    return article_results
# function to exatract just the name of the source of the news article and exclude other details


responses_list = [] # stores responses for various news sources instead of overwriting it
domains = ['wsj.com','aljazeera.com','bbc.co.uk','techcrunch.com', 'nytimes.com','bloomberg.com','businessinsider.com',
             'cbc.ca','cnbc.com','cnn.com','ew.com','espn.go.com','espncricinfo.com','foxnews.com', 'apnews.com',
             'news.nationalgeographic.com','nymag.com','reuters.com','rte.ie','thehindu.com','huffingtonpost.com',
             'irishtimes.com','timesofindia.indiatimes.com','washingtonpost.com','time.com','medicalnewstoday.com',
             'ndtv.com','theguardian.com','dailymail.co.uk','firstpost.com','thejournal.ie', 'hindustantimes.com',
             'economist.com','news.vice.com','usatoday.com','telegraph.co.uk','metro.co.uk','mirror.co.uk','news.google.com']
for domain in domains:
    parameters_headlines = {
    'domains':format(domain),
    'sortBy':'popularity',
    'pageSize': 100,
    'apiKey': api_key,
    'language': 'en',
    'from' : date
    }
    rr = requests.get(url, params = parameters_headlines)
    data = rr.json()

    responses = data["articles"]
    # print(responses)
    # Append the DataFrame to the list
    responses_list.append(pd.DataFrame(get_articles(responses)))

# Concatenate all DataFrames in the list into a single DataFrame
news_articles_df = pd.concat(responses_list, ignore_index=True)

def source_getter(df):
    source = []
    for source_dict in df['source']:
        source.append(source_dict['name'])
    df['source'] = source #append the source to the df
# this fuincton extracts the source name from the source dictionary as seen above
source_getter(news_articles_df)

# converted the publication date to date time format for future analysis
news_articles_df['pub_date'] = pd.to_datetime(news_articles_df['pub_date']).apply(lambda x: x.date())

# drop the rows that have missing data
print( "droping the rows with missing data")
news_articles_df.dropna(inplace=True)
news_articles_df = news_articles_df[~news_articles_df['description'].isnull()]
print(news_articles_df.isnull().sum())
print(news_articles_df.shape)

# combine the title and the content to get one dataframe column
news_articles_df['combined_text'] = news_articles_df['title'].map(str) +" "+ news_articles_df['content'].map(str)

# Function to remove non-ascii characters from the text
def _removeNonAscii(s):
    return "".join(i for i in s if ord(i)<128)
# function to remove the punctuations, apostrophe, special characters using regular expressions
def clean_text(text):
    text = text.lower()
    text = re.sub(r"what's", "what is ", text)
    text = text.replace('(ap)', '')
    text = re.sub(r"\'s", " is ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "cannot ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r'\W+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r"\\", "", text)
    text = re.sub(r"\'", "", text)
    text = re.sub(r"\"", "", text)
    text = re.sub('[^a-zA-Z ?!]+', '', text)
    text = _removeNonAscii(text)
    text = text.strip()
    return text
# stop words are the words that convery little to no information about the actual content like the words:the, of, for etc
def remove_stopwords(word_tokens):
    filtered_sentence = []
    stop_words = stopwords.words('english')
    specific_words_list = ['char', 'u', 'hindustan', 'doj', 'washington']
    stop_words.extend(specific_words_list )
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    return filtered_sentence
# function for lemmatization
def lemmatize(x):
    lemmatizer = WordNetLemmatizer()
    return' '.join([lemmatizer.lemmatize(word) for word in x])

# splitting a string, text into a list of tokens
tokenizer = RegexpTokenizer(r'\w+')
def tokenize(x):
    return tokenizer.tokenize(x)

# applying all of these functions to the our dataframe
news_articles_df['combined_text'] = news_articles_df['combined_text'].map(clean_text)
news_articles_df['tokens'] = news_articles_df['combined_text'].map(tokenize)
news_articles_df['tokens'] = news_articles_df['tokens'].map(remove_stopwords)
news_articles_df['lems'] =news_articles_df['tokens'].map(lemmatize)


# finding the keywords using the rake algorithm from NLTK
# rake is Rapid Automatic Keyword Extraction algorithm, and is used for domain independent keyword extraction
# news_articles_df['keywords'] = ""
# for index,row in news_articles_df.iterrows():
#     comb_text = row['combined_text']
#     r = Rake()
#     r.extract_keywords_from_text(comb_text)
#     key_words_dict = r.get_word_degrees()
#     row['keywords'] = list(key_words_dict.keys())
# # applying the fucntion to the dataframe
# news_articles_df['keywords'] = news_articles_df['keywords'].map(remove_stopwords)
# news_articles_df['lems'] =news_articles_df['keywords'].map(lemmatize)
news_articles_df.to_csv("assets/news_articles_clean.csv", index=False)