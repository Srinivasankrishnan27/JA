# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 01:13:17 2017

@author: krish
"""
import pandas as pd
import nltk
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.snowball import SnowballStemmer
import string
from nltk.corpus import stopwords
from nltk.corpus import opinion_lexicon
from nltk.tokenize import treebank
from sklearn.cluster import KMeans
import numpy as np

stemmer = SnowballStemmer("english")
review = []
category_list = []
nopunc = []
removStopwords = []
sentiment_score=[]

# review_collection : is the data frame which contains all the reviews scraped from the tripadvisor
review_collection=pd.read_csv("review_collection.csv",low_memory=False,encoding = "latin1")
review_collection_array=review_collection.values
review=review_collection_array[:,3]

def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems

def analyzesentiment(sentence):
    tokenizer = treebank.TreebankWordTokenizer()
    pos_words = 0
    neg_words = 0
    tokenized_sent = [word.lower() for word in tokenizer.tokenize(sentence)]
    keyword=[]
    for word in tokenized_sent:
        if word in opinion_lexicon.positive():
            pos_words += 1
            keyword.append(word)
        else:
            neg_words += 1
            keyword.append(word)
    if pos_words > neg_words:
        return('Positive',pos_words,neg_words,keyword)
    elif pos_words < neg_words:
        return('Negative',pos_words,neg_words,keyword)
    elif pos_words == neg_words:
        return('Neutral',pos_words,neg_words,keyword)

for i in range(0,len(review)):
    text_nopunc = review[i].translate((str.maketrans("", ""), string.punctuation)).lower()
    nopunc.append(review[i].translate((str.maketrans("", ""), string.punctuation)).lower())

stop = stopwords.words('english')

for i in range(0,len(nopunc)):
    removStopwords.append(" ".join(filter(lambda word: word not in stop, nopunc[i].split())))


ranks = []
for i in range(0,len(removStopwords)):
    ranks.append(i)

tfidf_vectorizer1Test = TfidfVectorizer(max_df=0.9, max_features=200000,
                                 min_df=0.05, stop_words='english',
                                 use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,3))
tfidf_matrix1Test = tfidf_vectorizer1Test.fit_transform(removStopwords)

num_clusters = 4
km1 = KMeans(n_clusters=num_clusters, random_state=23)
km1.fit(tfidf_matrix1Test)
clusters = km1.labels_.tolist()
terms = tfidf_vectorizer1Test.get_feature_names()
films = {'rank':ranks, 'title': removStopwords, 'cluster': clusters }
frame = pd.DataFrame(films, index = [clusters] , columns = ['rank','title', 'cluster'])
frame['cluster'].value_counts()
cluster1=frame[frame.cluster.isin([0])].values
cluster2=frame[frame.cluster.isin([1])].values
cluster3=frame[frame.cluster.isin([2])].values
cluster4=frame[frame.cluster.isin([3])].values
frame_array=frame.values

for i in range (len(frame_array)):
    sentiment, pos_count,neg_count,keyword=analyzesentiment(frame_array[i][1])
    sentiment_score.append((frame_array[i][1],frame_array[i][2],sentiment,pos_count,neg_count))

s=np.asarray(sentiment_score)
review_final=np.concatenate((review_collection_array,s),axis=1)
np.savetxt("review_final.csv",review_final,delimiter=",",newline="\n",fmt='%s')