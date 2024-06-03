import pickle
from fuzzywuzzy import fuzz
import numpy as np
import pandas as pd
from scipy import sparse
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from sklearn.linear_model import LogisticRegression
import warnings
warnings.filterwarnings("ignore")
from tkinter import *
from tabulate import tabulate
import argparse, sys

parser=argparse.ArgumentParser()

parser.add_argument('-user', '--userID', help='Enter existing/new UserID')

user_details = pd.read_pickle('user_details.pkl')
restaurant_details = pd.read_pickle('restaurant_details.pkl')
df_restaurants = pd.read_pickle('df_restaurants.pkl')

X=np.load('X.npy')
y=np.load('y.npy')

restaurant_to_idx = pickle.load(open("restaurant_to_idx.dic", "rb"))    

def load_sparse_csr(filename):
    loader = np.load(filename)
    return csr_matrix((loader['data'], loader['indices'], loader['indptr']),
                      shape=loader['shape'])

restaurant_user_mat_sparse=load_sparse_csr('restaurant_user_mat_sparse.npz')   

model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
model_knn.fit(restaurant_user_mat_sparse)

def fuzzy_matching(mapper, fav_rest, verbose=True):
    match_tuple = []
    for title, idx in mapper.items():
        ratio = fuzz.ratio(title.lower(), fav_rest.lower())
        if ratio >= 40:
            match_tuple.append((title, idx, ratio))
    match_tuple = sorted(match_tuple, key=lambda x: x[2])[::-1]
    return match_tuple[0][1]

def make_recommendation(model_knn, data, mapper, fav_rest, n_recommendations):
    model_knn.fit(data)
    idx = fuzzy_matching(mapper, fav_rest, verbose=True)
    # inference
    distances, indices = model_knn.kneighbors(data[idx], n_neighbors=n_recommendations+1)
    # get list of raw idx of recommendations
    raw_recommends = \
        sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())), key=lambda x: x[1])[:0:-1]
    # get reverse mapper
    reverse_mapper = {v: k for k, v in mapper.items()}
    final_list=[]
    # print recommendations
    print('Favorite Restaurant Name/Type: {}'.format(fav_rest))
    for i, (idx, dist) in enumerate(raw_recommends):
        final_list.append([reverse_mapper[idx], df_restaurants[df_restaurants['restaurant_name']==reverse_mapper[idx]].iloc[0]['business_id'],dist])
        #print('{0}: {1}, with distance of {2}'.format(i+1, reverse_mapper[idx], dist))
    return final_list

c_best=5054.4907871024025

clf = LogisticRegression(C=c_best).fit(X, y)

class ABC(Frame):
    def __init__(self,parent=None):
        Frame.__init__(self,parent)
        self.parent = parent
        self.pack()
        self.make_widgets()

    def make_widgets(self):
        # don't assume that self.parent is a root window.
        # instead, call `winfo_toplevel to get the root window
        self.winfo_toplevel().title("RECOMMENDER'S HUB")

args=parser.parse_args()
user=args.userID 
try:
    u_vec=list(user_details.loc[args.userID].profile_vector1)
except KeyError:
    u_vec=[0]*100
    user+=' (New User)'

root = Tk()
abc = ABC(root)
L = Label(root, text="User ID:", font=('calibri',(15)), width=35, height=3)
L.pack()
M = Label(root, text=user, font=('calibri',(15)), width=35, height=3)
M.pack()
L1 = Label(root, text="Fav Restaurant Name/Type:", font=('calibri',(15)), width=35, height=3)
L1.pack()
v=StringVar()
E1 = Entry(root, bd =5, font=('calibri',(15)), width=35, textvariable=v)
E1.pack()

def ok():
        root.destroy()

button = Button(root, text="Give Me Recommendations", command=ok)
button.config(width=38, height=3, bg='grey', font= 'Calibri 15')
button.pack()

root.mainloop()

#userID='uFVAAe0JC81IPmxgT49Hcw'
# userID=(username.var).get()
#my_favorite = 'Chipotle'
my_favorite = v.get()
reco_list =make_recommendation(
    model_knn=model_knn,
    data=restaurant_user_mat_sparse,
    fav_rest=my_favorite,
    mapper=restaurant_to_idx,
    n_recommendations=20)

rest_list=[]
for i in reco_list:
  r_vec=list(restaurant_details.loc[i[1]].profile_vector1)
  ypred = clf.predict(np.array([u_vec+r_vec]))[0]
  rest_list.append([i[0], i[2], ypred, i[2]*ypred])

rest_list.sort(key = lambda x: x[3], reverse = True)
Restaurants = pd.DataFrame(rest_list, columns=['Name', 'Distance[relevance]', 'Pred_Rating[fondness]', 'Hybrid_Rating'])
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
print('User ID:', user, '\nRecommendations:')
print(tabulate(Restaurants, headers='keys', tablefmt='psql'))
#print(Restaurants)                       