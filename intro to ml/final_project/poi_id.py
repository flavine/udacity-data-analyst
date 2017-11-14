#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
from sklearn.feature_selection import SelectKBest, SelectPercentile 

features_list = ['poi','salary', 'deferral_payments', 'total_payments', 'bonus',
                 'deferred_income', 'total_stock_value', 'expenses', 'exercised_stock_options', 
                 'long_term_incentive', 'restricted_stock', 'to_messages', 
                 'from_poi_to_this_person', 'from_messages', 'from_this_person_to_poi', 
                 'shared_receipt_with_poi']

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)


### Extract features and labels from dataset for plotting
plot_data = featureFormat(data_dict, features_list, sort_keys = True)
### Get feel of features to check outliers
import matplotlib.pyplot
for i in range(1,len(features_list)):
    for j in range(1,len(features_list)):
        if j>i:
            for point in plot_data:
                if point[0]==0:
                    matplotlib.pyplot.scatter( point[i], point[j],c='b' )
                if point[0]==1:
                    matplotlib.pyplot.scatter(point[i],point[j],c='r')
            matplotlib.pyplot.xlabel(features_list[i])
            matplotlib.pyplot.ylabel(features_list[j])
            #matplotlib.pyplot.show()

### Task 2: Remove outliers

# remove "Total" outlier
#Total row has the highest salary
current=0
for key in data_dict.keys():  
    if data_dict[key]['salary']>current and data_dict[key]['salary']!='NaN':
        total_outlier=key
        current=data_dict[key]['salary']
    
print total_outlier,current
del data_dict[total_outlier]

# Removing highest total_payments
# current2=0
# for key in data_dict.keys():  
#     if data_dict[key]['total_payments']>current and data_dict[key]['total_payments']!='NaN':
#         outlier2=key
#         current2=data_dict[key]['total_payments']
    
# print outlier2,current2
# del data_dict[outlier2]

#Check how many missing values we have per feature
missing_values = dict()

for i in range(0,len(features_list)):
    missing_values[features_list[i]]=0
    for key in data_dict.keys():
        if data_dict[key][features_list[i]]=='NaN':
            missing_values[features_list[i]]+=1
            
print missing_values
#print len(data_dict)
#print data_dict[outlier]

#look at how many NaNs there are for non-POIs and POIs
import pandas as pd

data = featureFormat(data_dict, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

nans = pd.DataFrame(0, index=[0,1], columns=features_list[1:])
for i in range(len(features)):
    label = int(labels[i])
    for j in range(len(features[i])):
        if features[i][j] == 0.0:
            nans.iloc[label,j] += 1
        
nans.T

### Task 3: Create new feature(s)

def computeFraction( poi_messages, all_messages ):
    """ given a number messages to/from POI (numerator) 
        and number of all messages to/from a person (denominator),
        return the fraction of messages to/from that person
        that are from/to a POI
   """
    fraction = 0.
    
    if all_messages == 'NaN':
        return fraction
    
    if poi_messages == 'NaN':
        poi_messages = 0
    
    fraction = 1.0*poi_messages/all_messages

    return fraction

#Create new features in data_dict
for k,v in data_dict.items(): 
    v['to_poi_frac']=computeFraction(v['from_this_person_to_poi'],v['to_messages'])
    v['from_poi_frac']=computeFraction(v['from_poi_to_this_person'],v['from_messages'])
    if v['to_messages']!='NaN' and v['from_messages']!='NaN':
        v['shared_recipient_frac']=computeFraction(v['shared_receipt_with_poi'],v['to_messages']+v['from_messages'])
    else:
        v['shared_recipient_frac']='NaN'
    print v 
    data_dict[k]=v

#Add new email_frac features in features_list and remove other email features
frac_features=['to_poi_frac','from_poi_frac','shared_recipient_frac']
features_list.extend(frac_features)
features_list.remove('from_this_person_to_poi')
features_list.remove('from_poi_to_this_person')
features_list.remove('from_messages')
features_list.remove('to_messages')
features_list.remove('shared_receipt_with_poi')

print features_list

### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)


### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn import svm
#from sklearn.grid_search import GridSearchCV
#from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.model_selection import StratifiedShuffleSplit, GridSearchCV
from feature_format import featureFormat, targetFeatureSplit
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier

#Past models tried
#clf = GaussianNB()
#clf=tree.DecisionTreeClassifier(random_state = 1)
#clf=svm.SVC()
#clf = RandomForestClassifier(n_estimators=10, random_state=1, verbose=0)

#GridSearchCV for AdaBoostClassfier
parameters = {'learning_rate':[0.01, 0.1, 0.5, 1],'n_estimators':[25,50,75,100]}
model = AdaBoostClassifier(random_state=9)

#gs = GridSearchCV(model, parameters, verbose = 2, scoring='recall',
#                   cv= StratifiedShuffleSplit(n_splits=100, random_state=9) ,n_jobs = 3)
#gs.fit(features, labels)
#gs.best_params_
#gs.cv_results_


### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split

# features_train, features_test, labels_train, labels_test = \
#     train_test_split(features, labels, test_size=0.3, random_state=42)

#GridSearchCV for AdaBoostClassfier
parameters = {'learning_rate':[0.01, 0.1, 0.5, 1],'n_estimators':[25,50,75,100]}
model = AdaBoostClassifier(random_state=9)

#gs = GridSearchCV(model, parameters, verbose = 2, scoring='recall',
#                   cv= StratifiedShuffleSplit(n_splits=100, random_state=9) ,n_jobs = 3)
#gs.fit(features, labels)
#gs.best_params_
#gs.cv_results_

from sklearn.cross_validation import StratifiedShuffleSplit

clf = AdaBoostClassifier(random_state=7, n_estimators=75, learning_rate=1)
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)
cv = StratifiedShuffleSplit(labels, 1000, random_state = 42)

true_negatives = 0
false_negatives = 0
true_positives = 0
false_positives = 0

iteration = 0
for train_idx, test_idx in cv: 
    features_train = []
    features_test  = []
    labels_train   = []
    labels_test    = []
    for ii in train_idx:
        features_train.append( features[ii] )
        labels_train.append( labels[ii] )
    for jj in test_idx:
        features_test.append( features[jj] )
        labels_test.append( labels[jj] )

    clf.fit(features_train, labels_train)

    predictions = clf.predict(features_test)

    for prediction, truth in zip(predictions, labels_test):
        if prediction == 0 and truth == 0:
            true_negatives += 1
        elif prediction == 0 and truth == 1:
            false_negatives += 1
        elif prediction == 1 and truth == 0:
            false_positives += 1
        elif prediction == 1 and truth == 1:
            true_positives += 1
        else:
            print "Evaluating performance for processed predictions:"
            break

    
try:
    print true_negatives, false_negatives, false_positives, true_positives
    total_predictions = true_negatives + false_negatives + false_positives + true_positives
    accuracy = 1.0*(true_positives + true_negatives)/total_predictions
    precision = 1.0*true_positives/(true_positives+false_positives)
    recall = 1.0*true_positives/(true_positives+false_negatives)
    print accuracy,precision,recall
except:
    print "Got a divide by zero when trying out:", clf
    print "Precision or recall may be undefined due to a lack of true positive predicitons."


importances = clf.feature_importances_
import numpy as np
indices = np.argsort(importances)[::-1]
print 'Feature Ranking: '
for i in range(10):
    print "{} feature no.{} ({})".format(i+1,indices[i],importances[indices[i]]) 
print features_list

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)