import pandas
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import recall_score, precision_score 
from sklearn.metrics import accuracy_score
from time import time
import numpy as np
import matplotlib.pyplot as plt

col_names = ["duration","protocol_type","service","flag","src_bytes","dst_bytes","land","wrong_fragment",
"urgent","hot","num_failed_logins","logged_in","num_compromised","root_shell","su_attempted","num_root",
"num_file_creations","num_shells","num_access_files","num_outbound_cmds","is_host_login","is_guest_login",
"count","srv_count","serror_rate","srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate","diff_srv_rate",
"srv_diff_host_rate","dst_host_count","dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate",
"dst_host_same_src_port_rate","dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate",
"dst_host_rerror_rate","dst_host_srv_rerror_rate","label"]
df = pandas.read_csv("kddcup.data_10_percent_corrected", header=None, names = col_names)
print("Printing datafield description \n")
print('Importing Finished' + "\n")

################analysis of Training Data set###################
print("analysis of training data set \n")
print(df['label'].value_counts())

################Feature selection from set of data##############
num_features = [
    "duration","src_bytes",
    "dst_bytes","land","wrong_fragment","urgent","hot","num_failed_logins",
    "logged_in","num_compromised","root_shell","su_attempted","num_root",
    "num_file_creations","num_shells","num_access_files","num_outbound_cmds",
    "is_host_login","is_guest_login","count","srv_count","serror_rate",
    "srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
    "diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count",
    "dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate",
    "dst_host_rerror_rate","dst_host_srv_rerror_rate"
]
features = df[num_features].astype(float)
# print(features.describe())
print("\n")

#Feature is converted into float datatype
#grouping and set of normal and attack
labels = df['label'].copy()
labels[labels!='normal.'] = 'attack.'
print(labels.value_counts())
print("\n")


############## training our classifier using sklearn decision tree #################
clf = DecisionTreeClassifier()
t0 = time()
clf.fit(features,labels)
tt = time()-t0
print ("\n Classifier trained in {} seconds".format(round(tt,3)))
print('Now we have a trained system')
print('Loading Test Data' + "\n")
kdd_data_corrected = pandas.read_csv("corrected", header=None, names = col_names)
print(kdd_data_corrected['label'].value_counts())

#Analysis of Test Data
kdd_data_corrected['label'][kdd_data_corrected['label']!='normal.'] = 'attack.'
kdd_data_corrected['label'].value_counts()

labels = kdd_data_corrected['label'].copy()
labels[labels!='normal.'] = 'attack.'
print(labels.value_counts())

############ Feature selection and spliting of Testing data #############
from sklearn.model_selection import train_test_split 
features_train, features_test, labels_train, labels_test = train_test_split(
    kdd_data_corrected[num_features], 
    kdd_data_corrected['label'], 
    test_size=0.1, 
    random_state=42)

############# Prediction start here ##############
t0 = time()
pred = clf.predict(features_test)
tt = time() - t0
print("Predicted in {} seconds".format(round(tt,3)))

############# Calculating Rsquare ###############

acc = accuracy_score(pred, labels_test)
print ("R squared is {}.".format(round(acc,4)))

############# Calculating Accuracy ##############
acc_test = clf.score(features_test, labels_test) 
print ("Test Accuracy:", acc_test) # Test Accuracy: 0.9333

########## Calculating Precision and recall ###############

precision = precision_score(labels_test,pred, average="weighted")
recall = recall_score(labels_test, pred, average="weighted") 

print ("Precision:", precision) # Precision: 0.9496
print ("Recall:", recall) # Recall: 0.9333
