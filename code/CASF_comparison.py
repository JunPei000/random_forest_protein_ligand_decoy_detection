import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score
from random import shuffle
from timeit import default_timer as timer
import json

direct1 = Path_of_final_csv_folder
filenames = [i for i in os.listdir(direct2) if '.csv' in i and '.swp' not in i]
print (len(filenames))
shuffle(filenames)
print (filenames)
trainfiles, testfiles = train_test_split(filenames, train_size = 0.8, random_state = 42)
print (testfiles)
train_data = pd.DataFrame()
test_data = pd.DataFrame()
for tfile in trainfiles:
    print (tfile)
    train_data = train_data.append(pd.read_csv(direct2+tfile))
if 'Unnamed: 0.1' in train_data.columns:
        train_data = train_data.drop('Unnamed: 0.1', axis=1)
if 'Unnamed: 0' in train_data.columns:
        train_data = train_data.drop('Unnamed: 0', axis=1)
train_data = train_data.reset_index(drop=True)
print (train_data)
x_train = train_data.drop(['lig_name'], axis=1)
y_train = train_data['lig_name'].map(lambda x: 0 if x[-3:] == '000' else 1)
print(x_train)
print(y_train)
y_train=y_train.astype('float')

for tfile in testfiles:
    print (tfile)
    test_data = test_data.append(pd.read_csv(direct1+tfile))
if 'Unnamed: 0.1' in test_data.columns:
        test_data = test_data.drop('Unnamed: 0.1', axis=1)
if 'Unnamed: 0' in test_data.columns:
        test_data = test_data.drop('Unnamed: 0', axis=1)
test_data = test_data.reset_index(drop=True)
print (test_data)
x_test = test_data.drop(['lig_name'], axis=1)
y_test = test_data['lig_name'].map(lambda x: 0 if x[-3:] == '000' else 1)
print(x_test)
print(y_test)
y_test=y_test.astype('float')

clf =  RandomForestClassifier(criterion='gini', class_weight = {0:0.5, 1:0.5})
parameters = {
       'n_estimators':(1000, 5000),
       'max_depth':(100, 500),
       'min_samples_split':(2, 5),
       'min_samples_leaf':(1,2) }
grid_search = GridSearchCV(clf, parameters, cv=5,verbose=1,scoring='accuracy')
grid_search.fit(x_train, y_train)
print ('Best Training score: %0.3f' % grid_search.best_score_)
print ('Best parameters set:')
best_parameters = grid_search.best_estimator_.get_params()
for param_name in sorted(parameters.keys()):
    print ('\t%s: %r' % (param_name, best_parameters[param_name]))
predictions = grid_search.predict(x_test)
print ("Testing accuracy:",round(accuracy_score(y_test,predictions),4))
print ("\nComplete report of Testingdata\n",classification_report(y_test, predictions))
print ("\n\nRandom Forest Grid Search- Test Confusion Matrix\n\n",pd.crosstab( y_test, predictions,rownames = ["Actuall"],colnames = ["Predicted"]))

RMSD = []; RANK = []; conv_RMSD = {}; conv_RANK = {}; conv_test_rmsd = {}; conv_test_rank = {}; conv_ACC = {}; conv_test_acc = {}
fp_rank = open(Path_of_rank_result_for_all.json, 'r')
fp_rmsd = open(Path_of_rmsd_result_for_all.json, 'r')
fp_acc = open(Path_of_acc_result_for_all.json, 'r')
conv_RANK = json.load(fp_rank)
conv_RMSD = json.load(fp_rmsd)
conv_ACC = json.load(fp_acc)

for key in conv_RANK:
    conv_test_rmsd[key] = []
    conv_test_rank[key] = []
    conv_test_acc[key] = []
for tfile in testfiles:
    print (tfile)
    sysname = tfile.replace('result_', '').replace('.csv', '')
    for key in conv_RMSD:
        conv_test_rmsd[key].append(conv_RMSD[key][sysname+'_score.dat'])
        conv_test_rank[key].append(conv_RANK[key][sysname+'_score.dat'])
        conv_test_acc[key].append(conv_ACC[key][sysname+'_score.dat'])
    test_data = pd.DataFrame()
    test_data = test_data.append(pd.read_csv(direct1+tfile))
    if 'Unnamed: 0.1' in test_data.columns:
        test_data = test_data.drop('Unnamed: 0.1', axis=1)
    if 'Unnamed: 0' in test_data.columns:
        test_data = test_data.drop('Unnamed: 0', axis=1)
    class_1 = pd.DataFrame()
    class_1_orig = pd.DataFrame()
    class_0 = pd.DataFrame()
    class_0_orig = pd.DataFrame()
    test_data['class'] = test_data['lig_name'].map(lambda x: 0 if x[-3:] == '000' else 1)
    class_1_orig = test_data.loc[test_data['class'] == 1]
    class_1 = class_1_orig.drop(['class', 'lig_name'], axis=1)
    class_0_orig = test_data.loc[test_data['class'] == 0]
    class_0 = class_0_orig.drop(['class', 'lig_name'], axis=1)
    if 2*len(class_1.index) != len(test_data.index):
        print ('Error! Check file :', tfile)
    native_score = 0
    native_prediction = grid_search.predict(class_0)
    native_score = sum(native_prediction)
    scores = []; names = [];
    for row in class_1.index:
        ddf1 = pd.DataFrame(columns = class_1.columns, index = class_1.index)
        ddf2 = pd.DataFrame(columns = class_1.columns, index = class_1.index)
        ddf_final = pd.DataFrame(columns = class_1.columns, index = class_1.index)
        ddf1.loc[[d1 for d1 in class_1.index],:] = class_1.loc[row].values
        ddf2.loc[[d2 for d2 in class_1.index if d2 != row],:] = class_1.loc[[d3 for d3 in class_1.index if d3 != row],:].values
        ddf2 = ddf2.fillna(0)
        ddf_final = ddf1.sub(ddf2)
        predictions = grid_search.predict(ddf_final)
        sc = sum(predictions)
        #print (sc)
        scores.append(sc)
        names.append(class_1_orig.loc[row, 'lig_name'].replace('111', ''))
    scores.append(native_score)
    names.append('native')
    print (sorted(scores).index(native_score)+1)
    RANK.append(sorted(scores).index(native_score)+1)
    decoy_score = []
    decoy_score = scores[:-1]
    decoy_names = []
    decoy_names = names[:-1]
    decoy_name = decoy_names[decoy_score.index(min(decoy_score))]
    print (decoy_name)
    fp_d = open(Path_of_CASF-2013_power_docking+'/'+sysname+'_rmsd.dat', 'r').readlines()
    for line in fp_d:
        if decoy_name+' ' in line:
            newlist = []
            newlist = line.split()
    RMSD.append(float(newlist[-1].replace('\n', '')))

print ('native ranking :\n')
for i in RANK:
    print (i)
print ('1st decoy rmsd :\n')
for i in RMSD:
    print (i)
print ('conventional results: \n')
for key in conv_test_rmsd:
    print (key)
print ('conventional RMSD :\n')
for key in conv_test_rmsd:
    print (sum(conv_test_rmsd[key])/len(conv_test_rmsd[key]))
print ('conventional Ranking :\n')
for key in conv_test_rank:
    print (sum(conv_test_rank[key])/len(conv_test_rank[key]))
print ('conventional accuracy :\n')
for key in conv_test_acc:
    print (sum(conv_test_acc[key])/len(conv_test_acc[key]))

