#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import matplotlib
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import numpy as np
import sklearn.svm
import math
#from sklearn.utils.class_weight import compute_class_weight
# import sys
# sys.path.append('Desktop/Class documents/Spring 2020/MATH 485/Project/GitHubStuff')
# import crx


# ## Get Categorical Data as Discrete integer data

# In[3]:

from lib.crxPandas import crx_data

# ## Put data in dataframe and manipulate columns
# #### Make Approved column last

# In[75]:


data = pd.DataFrame(crx_data)
# cols = data.columns.to_list()
# cols = cols[0:1] + cols[2:] + cols[1:2]
# data = data[cols]


# 5 most important features from Lasso Regression: <br>
#     1) Ethnicity <br>
#     2) YearsEmployed <br>
#     3) PriorDefault <br>
#     4) Employed <br>
#     5) CreditScore <br>

# In[68]:


# # using 5 most important from Lasso Regression
cols = ['Ethnicity','YearsEmployed','PriorDefault','Employed','CreditScore','Approved']
# # using only 4 most important
# #cols = ['Ethnicity','YearsEmployed','PriorDefault','Employed','Approved']
# # using 6 most important
# #cols = ['Ethnicity','YearsEmployed','PriorDefault','Employed','CreditScore','Debt','Approved']
data = data[cols]


# In[71]:


# using 4 most important from Kuhn Paper
# cols = ['Income','YearsEmployed','PriorDefault','CreditScore','Approved']
# data = data[cols]


# In[76]:


# using 6 most important from CART model
# cols = ['ZipCode','PriorDefault','Employed', 'Debt','Citizen','Income','Approved']
# data = data[cols]


# ## Save manipulated data as csv

# In[110]:


#data.to_csv('/Users/ethanweiss/Desktop/Class Documents/Spring 2020/MATH 485/Project/mod_data.csv')


# In[4]:


# read data from csv file
#data = pd.read_csv('/Users/ethanweiss/Desktop/Class documents/Spring 2020/MATH 485/Project/mod_data.csv')


# ## Change Data to Numpy array and Split into test and train sets
# #### Train/Test split = 80/20

# In[5]:


# transform pandas dataframe to numpy array
np_data = data.to_numpy()


# In[6]:


def shuffle_in_unison(a, b):
    assert len(a) == len(b)
    shuffled_a = np.empty(a.shape, dtype=a.dtype)
    shuffled_b = np.empty(b.shape, dtype=b.dtype)
    permutation = np.random.permutation(len(a))
    for old_index, new_index in enumerate(permutation):
        shuffled_a[new_index] = a[old_index]
        shuffled_b[new_index] = b[old_index]
    return shuffled_a, shuffled_b


# In[7]:


X = np_data[:,:-1]
y = np_data[:,-1:]
X,y = shuffle_in_unison(X,y)
train_X = X[:math.floor(len(X)*.8),:]
train_y = y[:math.floor(len(X)*.8),:]
test_X = X[math.floor(len(X)*.8):,:]
test_y = y[math.floor(len(X)*.8):,:]
train_y = np.ravel(train_y)
print(train_X.shape)
print(train_y.shape)


# ## Train SVM model
# Things changed: <br>
#     1) kernel = 'rbf' vs. 'sigmoid' <br>
#     2) class_weight = 'balanced' vs. 'NONE' <br>
#     3) probability = True --> model.predict_proba vs. model.predict results <br>
#     4) gamma = 'scale' vs. 'auto' <br>
#     5) k-fold validation vs. not

# Most important features from paper: <br>
#     1) Employed <br>
#     2) CreditScore <br>
#     3) Income <br>

# In[16]:


model = sklearn.svm.SVC(kernel = 'sigmoid',probability = True,class_weight = 'balanced',gamma = 'scale')
model.fit(train_X,train_y)


# In[34]:


model.get_params()


# ## Predict on Train Data from trained SVM Model
# ### Evaluate performance by checking prediction accuracy

# In[43]:


# proba_predictions = model.predict_proba(test_X)
# #predictions = model.predict(test_X)
# prob_predictions = [0 if x>=.7 else 1 for (x,y) in proba_predictions]
# test_y = np.ravel(test_y)
# correct_pred = []
# for (x,y) in zip(prob_predictions,test_y):
#     if x == y:
#         correct_pred.append(1)
#     else:
#         correct_pred.append(0)
# print(sum(correct_pred)/len(correct_pred) * 100)


# In[15]:


# model.score(test_X,test_y)


# In[37]:


# pred_data = pd.DataFrame(columns = ['Predicted','Actual'])
# pred_data['Predicted'] = predictions
# pred_data['Actual'] = test_y


# In[38]:


# pred_data[pred_data['Predicted'] == 1]


# ### Testing k-fold validation

# In[77]:


# transform pandas dataframe to numpy array
np_data = data.to_numpy()
X = np_data[:,:-1]
y = np_data[:,-1:]
X,y = shuffle_in_unison(X,y)
X_folds = np.array_split(X,5)
y_folds = np.array_split(y,5)
scores = list()
model = sklearn.svm.SVC(kernel = 'rbf',probability = True,class_weight = 'balanced',gamma = 'scale')
for k in range(5):
    X_train = list(X_folds)
    X_test = X_train.pop(k)
    X_train = np.concatenate(X_train)
    y_train = list(y_folds)
    y_test = np.ravel(y_train.pop(k))
    y_train = np.ravel(np.concatenate(y_train))
    scores.append(model.fit(X_train,y_train).score(X_test,y_test))
print(scores)
import statistics
print('Average Score: {0}'.format(statistics.mean(scores)))
# train_X = X[:math.floor(len(X)*.8),:]
# train_y = y[:math.floor(len(X)*.8),:]
# test_X = X[math.floor(len(X)*.8):,:]
# test_y = y[math.floor(len(X)*.8):,:]
# train_y = np.ravel(train_y)
# print(train_X.shape)
# print(train_y.shape)


# In[ ]:




