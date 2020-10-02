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

    positif=df[df['label']>3].sample(391)

    negatif=df[df['label']<3]

    Corpus=pd.concat([positif,negatif],ignore_index=True)[['review','label']]

    for ind in Corpus['label'].index:
      if Corpus.loc[ind,'label'] > 3:
          Corpus.loc[ind,'label']=1
      elif Corpus.loc[ind,'label'] < 3:
          Corpus.loc[ind,'label']=0
      pass


    my_stop_word_list = get_stop_words('french')

    s_w=list(set(my_stop_word_list))
    s_w=[elem.lower() for elem in s_w]

    nettoyage(Corpus['review'].loc[1])

    Corpus['review_net']=Corpus['review'].apply(nettoyage)

    vectorizer = TfidfVectorizer()
    vectorizer.fit(Corpus['review_net'])
    X=vectorizer.transform(Corpus['review_net'])

    #Save vectorizer.vocabulary_
    pickle.dump(vectorizer.vocabulary_,open("feature.pkl","wb"))

    self.vectorizer = vectorizer

    y=Corpus['label']

    x_train, x_val, y_train, y_val = train_test_split(X, y, test_size = 0.2)

    cls=LogisticRegression(max_iter=300).fit(x_train,y_train)
    #Save classifier
    pickle.dump(cls,open("cls.pkl","wb"))

    transformer = TfidfTransformer()
    loaded_vec = CountVectorizer(decode_error="replace",vocabulary=pickle.load(open("feature.pkl", "rb")))
    # user = transformer.fit_transform(loaded_vec.fit_transform([nettoyage(self.sentiment)]))
    # self.user = user
    cls=pickle.load(open("cls.pkl", "rb"))
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
    pass

  def evaluate_sentiment(self, phrase):

    self.user = self.vectorizer.transform([nettoyage(phrase)])

    if self.cls.predict(self.user)[0] == 0.0:
      return 'Désolé que vous ayez passé un mauvais moment'
      pass
    else:
      return 'Au plaisir de vous revoir'
      pass

  pass
