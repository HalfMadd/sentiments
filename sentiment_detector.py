import pandas as pd
import matplotlib.pyplot as plt
import pickle
import numpy as np
import re

from sklearn.feature_extraction.text import TfidfVectorizer,TfidfTransformer,CountVectorizer
from nltk.stem import SnowballStemmer
from stop_words import get_stop_words
from unidecode import unidecode
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

from nettoyage import nettoyage

class Sentiment:

  def __init__(self):
    super().__init__()
    df=pd.read_csv('corpus.csv')
    df['l_review']=df['review'].apply(lambda x:len(x.split(' ')))
    df[(df['rating']<3) & (df['l_review']>5)].describe()
    df=df[df['l_review']>5]
    df['label']=df['rating']


    for ind in df['label'].index:
      if df.loc[ind,'label'] >= 3:
          df.loc[ind,'label']=1
      elif df.loc[ind,'label'] < 3:
          df.loc[ind,'label']=0
      pass

    positif=df[df['label'] == 1].sample(391)

    negatif=df[df['label'] == 0].sample(391)

    Corpus=pd.concat([positif,negatif],ignore_index=True)[['review','label']]
    print(Corpus['label'].value_counts())



    my_stop_word_list = get_stop_words('french')

    s_w=list(set(my_stop_word_list))
    s_w=[elem.lower() for elem in s_w]

    nettoyage(Corpus['review'].loc[1], s_w)

    Corpus['review_net']=Corpus['review'].apply(lambda x: nettoyage(x, s_w))

    vectorizer = TfidfVectorizer()
    vectorizer.fit(Corpus['review_net'])
    X=vectorizer.transform(Corpus['review_net'])

    pickle.dump(vectorizer.vocabulary_,open("feature.pkl","wb"))

    self.vectorizer = vectorizer

    y=Corpus['label']

    x_train, x_val, y_train, y_val = train_test_split(X, y, test_size = 0.2)

    cls=LogisticRegression(max_iter=300).fit(x_train,y_train)
    pickle.dump(cls,open("cls.pkl","wb"))

    self.s_w = s_w
    self.cls = cls
    self.X = X
    self.y = y
    pass

  def set_sentiment(self, sentiment):
    self.sentiment = sentiment
    pass

  def train_sentiment(self):
    x_train, x_val, y_train, y_val = train_test_split(self.X, self.y, test_size = 0.2)
    self.cls=LogisticRegression(max_iter=300).fit(x_train,y_train)
    pickle.dump(self.cls,open("cls.pkl","wb"))
    return int(self.cls.score(x_val, y_val) * 100)
    pass

  def evaluate_sentiment(self, phrase):

    self.user = self.vectorizer.transform([nettoyage(phrase, self.s_w)])
    return int(self.cls.predict(self.user))[0]
    pass

  pass
