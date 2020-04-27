#!/usr/bin/env python
# coding: utf-8

# In[158]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# In[161]:


data = pd.read_csv('../crx.data',names = ['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12','A13','A14','A15','A16'])


# In[162]:


a1 = data.loc[:,'A1'].to_list()
for i in range(len(a1)):
    if a1[i] == 'b':
        a1[i] = 1
    elif a1[i] == 'a':
        a1[i] = 0
    else:
        a1[i] = float('nan')
data['A1'] = a1


# In[163]:


a2 = data.loc[:,'A2'].to_list()
a14 = data.loc[:,'A14'].to_list()
for i in range(len(a2)):
    try:
        a2[i] = float(a2[i])
    except:
        a2[i] = float('nan')
    try:
        a14[i] = float(a14[i])
    except:
        a14[i] = float('nan')
data['A2'] = a2
data['A14'] = a14


# In[164]:


a4 = data.loc[:,'A4'].to_list()
for i in range(len(a4)):
    if a4[i] == '?':
        a4[i] = float('nan')
data['A4'] = a4


# In[165]:


a5 = data.loc[:,'A5'].to_list()
for i in range(len(a5)):
    if a5[i] == '?':
        a5[i] = float('nan')
data['A5'] = a5


# In[166]:


a6 = data.loc[:,'A6'].to_list()
for i in range(len(a6)):
    if a6[i] == '?':
        a6[i] = float('nan')
data['A6'] = a6


# In[167]:


a7 = data.loc[:,'A7'].to_list()
for i in range(len(a7)):
    if a7[i] == '?':
        a7[i] = float('nan')
data['A7'] = a7


# In[168]:


a16 = data.loc[:,'A16'].to_list()
for i in range(len(a16)):
    if a16[i] == '+':
        a16[i] = 1
    else:
        a16[i] = 0
data['A16'] = a16


# In[169]:


data.to_csv('../crxTransformed.csv',index = False)


# In[ ]:




