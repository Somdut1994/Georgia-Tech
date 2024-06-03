import nltk.data
import pandas as pd
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.metrics import f1_score

from warnings import filterwarnings
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression

from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt

import os
import time
import math
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from fuzzywuzzy import fuzz
import seaborn as sns
plt.style.use('ggplot')

import pickle

import nltk
nltk.download('punkt')

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
import warnings
warnings.filterwarnings("ignore")

from scipy import sparse

train = pd.read_csv( "Avondale_Restaurant_Review.csv", delimiter=",", engine='python')

def clean_review(review, remove_stopwords = False):
    # 1. Remove HTML
    review_text = BeautifulSoup(review).get_text()
    #  
    # 2. Remove non-letters
    review_text = re.sub("[^a-zA-Z]"," ", review_text)
    #
    # 3. Convert words to lower case and split them
    cleaned_review = review_text.lower().split()
    #
    # 4. Optionally remove stop words (false by default)
    if remove_stopwords:
        stops = set(stopwords.words("english"))
        cleaned_review = [w for w in cleaned_review if not w in stops]

    return cleaned_review

from gensim.models import FastText

def review_to_sentences( review: str, tokenizer: nltk.tokenize.punkt.PunktSentenceTokenizer ):
    # 1. Use the NLTK tokenizer to split the paragraph into sentences
    raw_sentences = tokenizer.tokenize(review.strip())
    #
    # 2. Loop over each sentence
    review_sentences = []
    for raw_sentence in raw_sentences:
        # If a sentence is empty, skip it
        if len(raw_sentence) > 0:
            # Otherwise, call review_to_wordlist to get a list of words
            review_sentences.append(clean_review(raw_sentence))    
    ######################
    
    return review_sentences

sentences = []
for review in train["text"]:
    sentences += review_to_sentences(review, tokenizer)    

def generate_z(sentences):
    model = FastText(sentences, size=100, window=5, min_count=5, workers=4,sg=1)
    word_list = list(model.wv.vocab)
    z=np.array([model[word] for word in word_list])  

    return model, z, word_list       

model, z, word_list = generate_z(sentences)
    
def text2vec(model, text): 
  n=0 
  vec=np.zeros(100)
  for token in cr:
    try:
      v=model[token]
    except KeyError:
      continue
    n+=1.0
    for i in range(vec.shape[0]):
        vec[i]+=v[i]
  if n>0:
    for i in range(vec.shape[0]):
      vec[i]/=n
  return vec

def split(X, label):
    x_train, x_test, y_train, y_test = train_test_split(X, label, test_size = 0.2, random_state=0)
    return x_train, x_test, y_train, y_test

user_details = train[['user_id', 'text']].groupby(['user_id']).sum()
restaurant_details = train[['business_id', 'text']].groupby(['business_id']).sum()

user_profile1=[]
num_reviews = user_details["text"].size
for i in range(num_reviews):
    cr=clean_review(user_details["text"][i], remove_stopwords = True)
    user_profile1.append(text2vec(model, cr))

restaurant_profile1=[]
num_reviews = restaurant_details["text"].size
for i in range(num_reviews):
    cr=clean_review(restaurant_details["text"][i], remove_stopwords = True)
    restaurant_profile1.append(text2vec(model, cr))    

user_details.insert(1, "profile_vector1", user_profile1, True) 
restaurant_details.insert(1, "profile_vector1", restaurant_profile1, True) 

user_details.to_pickle('user_details.pkl')
restaurant_details.to_pickle('restaurant_details.pkl')

num_reviews = train["text"].size
X2=[]
for i in range(num_reviews):
  u_vec=list(user_details.loc[train['user_id'][i]].profile_vector1)
  r_vec=list(restaurant_details.loc[train['business_id'][i]].profile_vector1)

  X2.append(u_vec+r_vec)

X2 = np.array(X2) 
y = train['stars'].as_matrix()
x2_train, x2_test, y_train, y_test = split(X2, y)

np.save('X.npy', x2_train)
np.save('y.npy', y_train)


df_restaurants = pd.read_csv( "Avondale_Restaurant_Review.csv", delimiter=",", engine='python',
                        usecols=['business_id', 'restaurant_name'],dtype={'business_id': 'str', 'restaurant_name': 'str'} )

df_restaurants.to_pickle('df_restaurants.pkl')

df_ratings = pd.read_csv("Avondale_Restaurant_Review.csv", delimiter=",", engine='python',
    usecols=['user_id', 'business_id', 'stars'],
    dtype={'user_id': 'str', 'business_id': 'str', 'stars': 'float32'})

df_restaurant_cnt = pd.DataFrame(df_ratings.groupby('business_id').size(), columns=['count'])

popularity_thres = 50
popular_restaurants = list(set(df_restaurant_cnt.query('count >= @popularity_thres').index))
df_ratings_drop_restaurants = df_ratings[df_ratings.business_id.isin(popular_restaurants)]

df_users_cnt = pd.DataFrame(df_ratings.groupby('user_id').size(), columns=['count'])

ratings_thres = 1
active_users = list(set(df_users_cnt.query('count >= @ratings_thres').index))
df_ratings_drop_users = df_ratings_drop_restaurants[df_ratings_drop_restaurants.user_id.isin(active_users)]

df_restaurants=df_restaurants.drop_duplicates()
df_ratings_drop_users=df_ratings_drop_users.drop_duplicates(['business_id','user_id'],keep= 'last')

restaurant_user_mat = df_ratings_drop_users.pivot(index='business_id', columns='user_id', values='stars').fillna(0)
restaurant_to_idx = {
    restaurant: i for i, restaurant in 
    enumerate(list(df_restaurants.set_index('business_id').loc[restaurant_user_mat.index].restaurant_name))
}

pickle.dump(restaurant_to_idx, open( "restaurant_to_idx.dic", "wb"))


# transform matrix to scipy sparse matrix
restaurant_user_mat_sparse = csr_matrix(restaurant_user_mat.values)



def save_sparse_csr(filename, array):
    np.savez(filename, data=array.data, indices=array.indices,
             indptr=array.indptr, shape=array.shape)


save_sparse_csr('restaurant_user_mat_sparse.npz', restaurant_user_mat_sparse)





