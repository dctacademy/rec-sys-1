
# coding: utf-8

# # Assignment "Assignment" System for DCT Academy's Code Platform

# In[1]:


import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import scipy.sparse as sparse
from sklearn.externals import joblib
from sklearn import metrics
import random
import implicit
import requests
import json


# ## Creating list of dataframe of all tables, a dictionary mapping to corresponding dataframe

# In[2]:


# Dictionary of all the tables and their columns
table_columns = {}

# Dictionary of all dataframes mapped with table names
df_all = {}

# List of all dataframes of all tables
df_list = []

request_tables = ['submissions', 'assignments', 'tags', 'taggings']

for table in request_tables:
    url = 'http://code.dctacademy.com/api/v1/ml/data/' + table + '?key=6eccc23db96ed84fce329e0d20bdacb4'
    response = requests.get(url)
#     print(response.status_code, response.reason)
    df_all[table] = pd.read_json(response.content)
    
model_path = '../ml-api/model/'


# ## Get all student/user assignments
# ### Merge submissions, assignments, taggings, tags

# In[3]:


user_submissions = df_all['submissions']     .merge(df_all['assignments'], left_on='assignment_id', right_on='id', suffixes=('_submissions', '_assignments'))     .merge(df_all['taggings'], left_on='id_assignments', right_on='taggable_id', suffixes=('_sub_ass', '_taggings'))     .merge(df_all['tags'], left_on='tag_id', right_on='id', suffixes=('_sub_ass_tag', '_tags')) 

submission_assignments = df_all['submissions']     .merge(df_all['assignments'], left_on='assignment_id', right_on='id', suffixes=('_submissions', '_assignments'))

user_submissions.drop(['statement', 'output', 'language', 'created_at_submissions', 'updated_at_submissions', 'is_checked', 'body', 'url', 
                       'created_at_assignments', 'updated_at_assignments', 'pass', 'fail', 'tagger_type', 'created_at', 'total', 'practice_id', 
                       'assignment_id', 'user_id_assignments', 'code_assignments', 'tagger_id', 'tag_id', 'source', 'input_size',
                       'approved', 'function_name', 'context', 'id_sub_ass_tag', 'taggings_count', 'is_allowed'], axis=1, inplace=True)


# In[4]:


user_submissions.columns


# In[5]:


user_submissions = user_submissions[user_submissions['taggable_type'] == 'Assignment']


# ### Cleaning tags and categories

# In[8]:


user_submissions['name'] = user_submissions['name'].str.strip().replace('/',',')


# In[12]:


user_submissions['time_in_seconds'] = user_submissions['time_in_seconds'].abs()


# ### Removing all submissions with time greater than 100,000 seconds

# In[13]:


median = user_submissions['time_in_seconds'].median() 
user_submissions.loc[user_submissions.time_in_seconds > 100000, 'time_in_seconds'] = np.nan
user_submissions.fillna(median, inplace=True)


# ### Getting submissions which are greater than 0 and lesser than 100000

# In[14]:


user_submissions = user_submissions[(user_submissions['time_in_seconds'] != 0) & (user_submissions['time_in_seconds'] < 100000)]


# In[17]:


user_submissions.reset_index(inplace=True)


# ### Creating the confidence column

# In[18]:


tags = df_all['tags']['name'].apply(lambda x:x.lower()).unique()
tags.sort()
tag_points = [10, 5, 15, 20, 15, 10, 25, 50, 20, 20, 100, 15, 20, 5, 5, 5, 75, 20, 15, 15, 5, 5, 10, 15, 5]

mapping = dict(zip(tags, tag_points))

assignment_tags = user_submissions.groupby(['id_assignments']).aggregate(lambda x: list(set(x)))['name'].to_frame()
assignment_points = assignment_tags['name'].apply(lambda x:[mapping[i] for i in x]).apply(lambda x:sum(x)).to_frame()


# In[19]:


user_submissions['assignment_points'] = user_submissions['id_assignments'].apply(lambda x: assignment_points.loc[x])
user_submissions['confidence'] = ((user_submissions['points_submissions'] / user_submissions['points_assignments']) + (user_submissions['minutes'] / (user_submissions['time_in_seconds'] / 60))) * user_submissions['assignment_points']


# ### Preparing for sparse matrix

# In[20]:


user_submissions = user_submissions.groupby(['user_id_submissions', 'id_assignments']).aggregate(lambda x:max(set(x)))['confidence'].reset_index()
user_submissions.to_csv(model_path + 'user_submissions.csv', index=False)


# ### Creating sparse matrix 

# In[21]:


user_submissions_pivot = user_submissions.pivot_table(values='confidence', index='id_assignments', columns='user_id_submissions', fill_value=0)
user_submissions_pivot.to_csv(model_path + 'user_submissions_pivot.csv')


# In[22]:


matrix_size = user_submissions_pivot.shape[0] * user_submissions_pivot.shape[1] 
interactions = user_submissions_pivot.astype(bool).sum(axis=0).sum()
sparsity = 100 * (1 - (interactions / matrix_size))


# ### Creating a Training and Validation Set

# #### Hide a certain percentage of the user/item interactions from the model_als during the training phase chosen at random.

# This function will take in the original user-assignment matrix and "mask" a percentage of the original id_assignments where a user-assignment interaction has taken place for use as a test set. The test set will contain all of the original assignments, while the training set replaces the specified percentage of them with a zero in the original assignments matrix. 
#     
# * **parameters**: 
#     
#     1. **id_assignments** - the original id_assignments matrix from which you want to generate a train/test set. Test is just a complete copy of the original set. This is in the form of a sparse csr_matrix. 
#     
#     2. **pct_test** - The percentage of user-assignment interactions where an interaction took place that you want to mask in the training set for later comparison to the test set, which contains all of the original id_assignments. 
#     
# * **returns**:
#     
#     1. **training_set** - The altered version of the original data with a certain percentage of the user-assignment pairs that originally had interaction set back to zero.
#     
#     2. **test_set** - A copy of the original id_assignments matrix, unaltered, so it can be used to see how the rank order compares with the actual interactions.
#     
#     3. **user_inds** - From the randomly selected user-assignment indices, which user rows were altered in the training data. This will be necessary later when evaluating the performance via AUC.

# In[23]:


def make_train(id_assignments, pct_test = 0.2):
    # Make a copy of the original set to be the test set. 
    test_set = id_assignments.copy() 
    
    # Store the test set as a binary preference matrix
    test_set[test_set != 0] = 1 
    
    # Make a copy of the original data we can alter as our training set. 
    training_set = id_assignments.copy() 
    
    # Find the indices in the assignments data where an interaction exists
    nonzero_inds = training_set.nonzero() 
    
    # Zip these pairs together of user,item index into list
    nonzero_pairs = list(zip(nonzero_inds[0], nonzero_inds[1])) 
    
    # Set the random seed to zero for reproducibility
    random.seed(0) 
    
    # Round the number of samples needed to the nearest integer
    num_samples = int(np.ceil(pct_test * len(nonzero_pairs))) 
    
    # Sample a random number of user-item pairs without replacement
    samples = random.sample(nonzero_pairs, num_samples) 
    
    # Get the user row indices
    user_inds = [index[0] for index in samples] 
    
    # Get the item column indices
    assignment_inds = [index[1] for index in samples] 
    
    # Assign all of the randomly chosen user-item pairs to zero
    training_set[user_inds, assignment_inds] = 0 
    
    # Get rid of zeros in sparse array storage after update to save space
    training_set.eliminate_zeros() 
    
    # Output the unique list of user rows that were altered  
    return training_set, test_set, list(set(user_inds)) 


# In[24]:


assignment_train, assignment_test, assignment_users_altered = make_train(sparse.csr_matrix(user_submissions_pivot.values), pct_test = 0.2)


# ### Saving the model_als

# In[25]:


model_als = implicit.als.AlternatingLeastSquares(factors=64, regularization = 0.1, iterations = 50)
model_als.fit(assignment_train)

user_vecs_als = model_als.item_factors
item_vecs_als = model_als.user_factors

filename = 'user_assignments_model_als.pkl'
joblib.dump(model_als, model_path + filename)


# ### Saving the model_bayes

# In[26]:


model_bayes = implicit.bpr.BayesianPersonalizedRanking(factors=95, learning_rate=0.2, regularization = 0.1, iterations = 50)
model_bayes.fit(assignment_train)

user_vecs_bayes = model_bayes.item_factors
item_vecs_bayes = model_bayes.user_factors

filename = 'user_assignments_model_bayes.pkl'
joblib.dump(model_bayes, model_path + filename)

