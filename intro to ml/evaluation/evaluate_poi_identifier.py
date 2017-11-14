#!/usr/bin/python


"""
    Starter code for the evaluation mini-project.
    Start by copying your trained/tested POI identifier from
    that which you built in the validation mini-project.

    This is the second step toward building your POI identifier!

    Start by loading/formatting the data...
"""

import pickle
import sys
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit

data_dict = pickle.load(open("../final_project/final_project_dataset.pkl", "r") )

### add more features to features_list!
features_list = ["poi", "salary"]

data = featureFormat(data_dict, features_list)
labels, features = targetFeatureSplit(data)



### your code goes here 


from sklearn.cross_validation import train_test_split
features_train,features_test,labels_train,labels_test=train_test_split(features,labels,test_size=0.3,random_state=42)

### it's all yours from here forward!  
from sklearn import tree 
from sklearn.metrics import accuracy_score
import numpy as np
clf=tree.DecisionTreeClassifier()
clf.fit(features_train,labels_train)
pred=clf.predict(features_test)
zeroes=29*[0]

def perf_measure(y_actual, y_hat):
    TP = 0
    FP = 0
    TN = 0
    FN = 0

    for i in range(len(y_hat)): 
        if y_actual[i]==y_hat[i]==1:
           TP += 1 
        elif y_actual[i]==y_hat[i]==0:
           TN += 1
        elif y_hat[i]==0 and y_actual!=y_hat[i]:
           FN += 1
        else:
          	FP += 1

	return(TP, FP, TN, FN)

#print accuracy_score(zeroes,labels_test)
#print perf_measure(labels_test,pred)

from sklearn.metrics import precision_score,recall_score
print precision_score(labels_test,pred),recall_score(labels_test,pred)
