# -*- coding: utf-8 -*-
"""Copy of CAP1990C Final Project - Bankruptcy.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/149PnT5NfxzBZUEkJYRj-in9pWMnZci1s
"""

# https://colab.research.google.com/drive/1frKGhhGeYSlIIxfmbZOHyaO_AQxmBZzs?usp=sharing#scrollTo=kGLd3nEREA0M

"""**Building a ML Model for the Bankruptcy Dataset**
---
- Joemichael Alvarez
- Frank Rodriguez
- Michael Seman


Here is the link to our dataset:
https://www.kaggle.com/datasets/fedesoriano/company-bankruptcy-prediction

With this dataset, we will build a ML model that predict if a company will go bankrupt or not.

We will perform EDA, Data Cleaning, Model Building, Testing, and Tuning.

A machine learning project may not be linear, but it has a number of well known steps:



1.   Define Problem
2.   Prepare Data
3.   Evaluate Algorithms
4.   Improve Results
5.   Present Results
"""

# Check the versions of libraries
 
# Python version
import sys
print('Python: {}'.format(sys.version))
# scipy
import scipy
print('scipy: {}'.format(scipy.__version__))
# numpy
import numpy as np
print('numpy: {}'.format(np.__version__))
# matplotlib
import matplotlib
print('matplotlib: {}'.format(matplotlib.__version__))
# pandas
import pandas as pd
print('pandas: {}'.format(pd.__version__))
# scikit-learn
import sklearn
print('sklearn: {}'.format(sklearn.__version__))

# Commented out IPython magic to ensure Python compatibility.
# Set the Environment
# Ignore Warnings
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#Write out the versions of all packages to requirements.txt
!pip freeze >> requirements.txt

# Remove the restriction on Jupyter that limits the columns displayed (the ... in the middle)
pd.set_option('max_columns',None)
pd.set_option('display.max_rows', None)
# Docs: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.set_option.html#

# Pretty Display of variables.  for instance, you can call df.head() and df.tail() in the same cell and BOTH display w/o print
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

# List of ALL Magic Commands.  To run a magic command %var  --- i.e.:  %env
# %lsmagic
# %env  -- list environment variables
# %%time  -- gives you information about how long a cel took to run
# %%timeit -- runs a cell 100,000 times and then gives you the average time the cell will take to run (can be LONG)
# %pdb -- python debugger

# to display nice model diagram
from sklearn import set_config
set_config(display='diagram')

# Python ≥3.5 is required
import sys
assert sys.version_info >= (3, 5)

# Scikit-Learn ≥0.20 is required
import sklearn
assert sklearn.__version__ >= "0.20"

"""**Load The Data**
---
We are going to use the iris flowers dataset. This dataset is famous because it is used as the “hello world” dataset in machine learning and statistics by pretty much everyone.

The dataset contains 150 observations of iris flowers. There are four columns of measurements of the flowers in centimeters. The fifth column is the species of the flower observed. All observed flowers belong to one of three species.

```
# This is formatted as code
```



"""

# Imported and loaded additional libraries

import matplotlib.pyplot as plt
import seaborn as sns
from pandas import read_csv
from pandas.plotting import scatter_matrix
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

# Loading the Dataset 

url = "https://github.com/AlvarezJoe/Datasets/raw/main/bankruptcy_data.csv"
df = read_csv(url)

"""**Summarize the Dataset**
---
Now it is time to take a look at the data. In this step we are going to take a look at the data a few different ways:



1.   Dimensions of the dataset.
2.   Peek at the data itself.
3.   Statistical summary of all attributes.
4.   Breakdown of the data by the class variable.

Don’t worry, each look at the data is one command. These are useful
commands that you can use again and again on future projects.

Dimensions of Dataset
---
We can get a quick idea of how many instances (rows) and how many attributes (columns) the data contains with the shape property.
"""

# The function below shows the dimensions of our dataset: 6819 rows and 96 different columns

df.shape

df.shape

# The head function gets the first n many rows and in the case below, I just wanted the first 2 rows so n = 2, just trying to take a peek into the data

df.head(2)

"""Statistical Summary
---
Now we can take a look at a summary of each attribute.This includes the count, mean, the min and max values as well as some percentiles.
"""

# Statistical description of each column/variable

df.describe()

"""Class Distribution
---
Let’s now take a look at the number of instances (rows) that belong to each class. We can view this as an absolute count.
"""

# The code below shows the amount of businesses (220) that went bankrupt and those that did not (6599), so like in most cases we have an imbalanced dataset
print(df.groupby('Bankrupt?').size())

"""# Additional Data Inspection & Cleaning

# Data inspection
"""

# Looking at the datatypes for each column in the dataframe to see if there are any categorical ones hiding as a numeric column
# Also checking at the same time if there are any null values in any of the columns, which after a review there does not seem to be

df.info()

df.dtypes.value_counts()

# Now checking to see how many unique values are in each column

df.nunique()

"""# Data Cleaning"""

# Realized that the Bankruptcy column is missing a space in the beginning the rest of the columns have and so I am using the strip method to remove any whitespace before and after the string of words in each column header

df.columns = df.columns.str.strip()

# Dropping the Net Income Flag because only has one unique value which is useless in any kind of model and moving the 'Liability-Assets Flag' column as it looks like a categorical variable disguised as numeric/continuous variable with only 2 unique values
#netInCol = df['Net Income Flag']
df.drop(labels=['Net Income Flag'], axis=1, inplace = True)
#df.insert(len(df.columns),'Net Income Flag', netInCol)

LAFlag = df['Liability-Assets Flag']
df.drop(labels=['Liability-Assets Flag'], axis=1, inplace = True)
df.insert(len(df.columns),'Liability-Assets Flag', LAFlag)

# On a recomendation from Dr Lee, with 96 different columns I decided to create a dictionary of the column names indexed by numbers. 
# I will now replace the current column names in the dataset, to use the column indexes more effeciently and also not lose the context of what each column means

columnIndexDict = {}
colNum = 0

for col in df.columns: 
  columnIndexDict[colNum] = col
  colNum += 1

columnIndexDict

# Changing the column names into numbers to work with them more easily
i = 0

for col in df:
  
  if columnIndexDict[i] == col:
    df.rename(columns = {col:i}, inplace = True)
    i += 1

# Just to confirm that the change worked

df.head(2)

df[0].value_counts()

df_X = df.loc[:, 1:len(df)]
df_y = df.loc[:,0]

df_X.head(1)

"""# Basic Visualizations

## Univariate Plots

We are going to visualize our first four columns to just get a better idea of the data we are working with.

**First, let's see some histograms to see how our values are distributed.**
"""

for i in range(1,5):
  plt.figure(figsize =(2, 2))
  df[i].hist()
  title = columnIndexDict[i]
  plt.title(title)
plt.show()

"""**Now let's do some box plots.**"""

for i in range(1,5):
  plt.figure(figsize =(3, 3))
  plt.boxplot( df[i])
  title = columnIndexDict[i]
  plt.title(title)
plt.show()

"""**Let's look at our next 4 columns as histograms grouped together**"""

data = df.iloc[:,5:9]
data.hist()
pyplot.show()
# we are checking for a normal distribition here.  The first 3 seems great, we might need to look into column 4.

# double checking to make sure these columns don't contain the same values
df.iloc[:,5:9].nunique()

"""Multivariate Plots
---
Now we can look at the interactions between the variables. First, let’s look at scatterplots of all pairs of attributes. This can be helpful to spot structured relationships between input variables.
"""

# scatter plot matrix
scatter_matrix(data)
pyplot.show()
#Note the diagonal grouping of some pairs of attributes. This suggests a high correlation and a predictable relationship.

"""## Correlations"""

# Not the easiest to read, but for fun lets make a heat map of ALL the correlations for our dataset
corrmat = df.corr()
top_corr_features = corrmat.index
plt.figure(figsize=(20,20))
# plot heat map
g = sns.heatmap(df[top_corr_features].corr(), annot=False, cmap='RdYlGn')

# now lets focus on the only important column's correlation, our target variable (Bankrupt) with our features
plt.figure(figsize=(5,20))
x = corrmat[[0]]
x = x.iloc[1:,:]
sns.heatmap(x, annot=True,cmap='RdYlGn')

# now lets look at the top 10 highest and lowest correlations.
x = x.sort_values(by=[0])
print("Top 10 Negative Correlations: ", x[0:10])
print("Top 10 Positive Correlations: ",x[len(x)-10:])

"""# Creating a model

## Splitting the Data
A simple 80/20 split.
"""

# Split-out validation dataset
X_trainh, X_validationh, Y_trainh, Y_validationh = train_test_split(df_X, df_y, test_size=0.20, random_state=1)

"""## Harness

We are going to send our data through a harness to test the Accuracy of 8 different algorithms:
1.   Logistic Regression (LR).
2.   Linear Discriminant Analysis (LDA).
3.   K-Nearest Neighbors (KNN). 
4.   Classification and Regression Trees (CART).
5.   Gaussian Naive Bayes (NB).
6.   Support Vector Machine (SVM).
7.   XGBoost (XGB).
8.   Random Forest (RFC).

"""

# was thinking of using catboost, but in the end it just takes too long
!pip install catboost
from catboost import CatBoostClassifier
# models.append(('CAT', CatBoostClassifier(verbose=0, boosting_type='Plain',leaf_estimation_iterations=1)))

from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier

# Creating Models
models = []
models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC(gamma='auto')))
models.append(('XGB', XGBClassifier()))
models.append(('RFC', RandomForestClassifier()))


# evaluate each model based on accuracy score using stratified kfold
results = []
names = []
for name, model in models:
	kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
	cv_results = cross_val_score(model, X_trainh, Y_trainh, cv=kfold, scoring='accuracy')
	results.append(cv_results)
	names.append(name)
	print('%s: %f accuracy ' % (name, cv_results.mean()))
	# print('%s: %f accuracy (%f) std' % (name, cv_results.mean(), cv_results.std()))

"""Select Best Model
---
Above we have the accuracy scores for our 8 models.  Let's visualize them so we can inform our selection for the best model.
"""

# Compare Accuracies with Box plots
pyplot.figure(figsize=(6,5))
pyplot.boxplot(results, labels=names)
pyplot.title('Algorithm Comparison')
pyplot.show()
# This isn't the best visualization.  We can clearly see the NB (Naive Bayes) is the worst
# maybe if we remove it, we can see the rest better

# removing NB from the results and labels
results2, names2 = results, names
results2.pop(4)
names2.pop(4)

# Compare Algorithms again minus NB
pyplot.figure(figsize=(6,5))
pyplot.boxplot(results2, labels=names2)
pyplot.title('Algorithm Accuracy')
pyplot.show()
# Now we can see our top performing models much better

"""**Make Predictions**
---
Let's look at SVM, RFC, and XGB and see how well they make predictions (our most accurate models).
"""

# fitting model SVC
model = SVC(gamma='auto')
model.fit(X_trainh, Y_trainh)
predictions = model.predict(X_validationh)

# fitting model rfc
model_rfc = RandomForestClassifier()
model_rfc.fit(X_trainh, Y_trainh)
predictions_rfc = model_rfc.predict(X_validationh)

xgb_clf = XGBClassifier()
xgb_clf.fit(X_trainh, Y_trainh)
predictions_xgb = xgb_clf.predict(X_validationh)

"""Evaluate Predictions
---
Let's look at our confusion matrices and classification reports for our selected models and evaluate how our models did at predicting.
"""

# Evaluate predictions for Support Vector Machine
print(confusion_matrix(Y_validationh, predictions))
print(classification_report(Y_validationh, predictions))

# Evaluate predictions for Random Forest
print(confusion_matrix(Y_validationh, predictions_rfc))
print(classification_report(Y_validationh, predictions_rfc))

# Evaluate predictions for XGBoost
print(confusion_matrix(Y_validationh, predictions_xgb))
print(classification_report(Y_validationh, predictions_xgb))

Y_validationh.value_counts(normalize=True)

"""### Initial Observations:
Looking at models solely based on accuracy can be misleading.  The most important part of our model is correctly classifying the Yes class.  The data is very imbalanced, so it's easy to be accurate.  If you simply predicted the majority class (No), your accuracy would be 96%.  Only XGBoost and Random Forest outperform that.

## Harness 2 (with Recall of Yes class as metric)
"""

from sklearn.metrics import make_scorer
from sklearn.metrics import recall_score
recall_scorer = make_scorer(recall_score, pos_label=1)

results2 = []
names2 = []
for name, model in models:
	kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
	cv_results = cross_val_score(model, X_trainh, Y_trainh, cv=kfold, scoring=recall_scorer)
	results2.append(cv_results)
	names2.append(name)
	# print('%s: %f recall ' % (name, cv_results.mean()))
	print('%s: %f recall (%f) std' % (name, cv_results.mean(), cv_results.std()))

# Compare Algorithms with Box plots
pyplot.figure(figsize=(6,5))
pyplot.boxplot(results2, labels=names2)
pyplot.title('Algorithm Recall-Yes Comparison')
pyplot.show()

modelNB = GaussianNB()
modelNB.fit(X_trainh, Y_trainh)
predictions_NB = modelNB.predict(X_validationh)

# Evaluate predictions for NB
print(confusion_matrix(Y_validationh, predictions_NB))
print(classification_report(Y_validationh, predictions_NB))

"""## Most Important Features"""

def feature_imp(df, model):
    fi = pd.DataFrame()
    fi["feature"] = df.columns
    fi["importance"] = model.feature_importances_
    return fi.sort_values(by="importance", ascending=False)

df_features = feature_imp(df_X, xgb_clf)[:25]
df_features.set_index('feature', inplace=True)
df_features.plot(kind='barh', figsize=(10, 8))
plt.title('Feature Importance according to XGBoost')

df_features.index

# saving the top 25 features in a dataframe in case we need to use them later
df_top25 = df[df_features.index]
df_top25.head()

"""Final Observations
---

- A Dummy Model would predict at 96.3% accuracy.
- Most of our models performed at this level, meaning they would be just as accurate simply predicted the majority class (No) every time.
- After pulling the classification reports and confusion matrix, we can see that accuracy is not the most meaningful stat for this dataset.
- We compared recall scores, and our worst performing model in accuracy had the best recall (Naive Bayes).
- Unfortunately NB essentially predicted the minority class every time, resulting in a very low recall for the no class, and low precision for the yes class.
- For accuracy, the models that most deserve further analysis are Support Vector Machine, XGBoost, and Random Forest Classifier.
- For recall, the models that most deserve further analysis are Linear Discriminate Analysis, Decision Tree, and XGBoost.
- XGBoost specifically will be explored later as it appears in both lists.

# A Deep Dive - XGBoost
## Dealing with Imbalanced Data
"""

# splitting the data
X_train, X_test, y_train, y_test = train_test_split(df_X, df_y, test_size=0.20, random_state=1,stratify=df_y)

"""## Baseline"""

xgb = XGBClassifier()

xgb.fit(X_train, y_train)

pred =xgb.predict(X_test)

"""### Results:"""

confusion_matrix (y_test, pred)

print (classification_report (y_test, pred))

"""## Under Sampling"""

# combining data for ease of use
trainData = pd.concat([X_train,y_train],axis=1)
# finding indexes where bankrupt = 1 (yes)
ind = trainData[trainData[0]==1].index
# finding indexes of majority class
ind1 = trainData[trainData[0]==0].index
# separating minority class
minData = trainData.loc[ind]
# separating majority class
majData = trainData.loc[ind1]
# Take a random sample equal to length of the minority class to make the data set balanced
majSample = majData.sample(n=len(ind),random_state = 123)

trainData[0].value_counts()

balData = pd.concat([minData,majSample],axis = 0)
print('balanced data set shape',balData.shape)

# Shuffling the data set
from sklearn.utils import shuffle
balData = shuffle(balData)

# Making the new X_train and y_train
X_trainNew = balData.iloc[:,:-1]
y_trainNew = balData[0]

# Defining New Model
xgb_us = XGBClassifier()
xgb_us.fit(X_trainNew, y_trainNew)

y_pred2 = xgb_us.predict(X_test)

"""### Results:"""

confusion_matrix (y_test, y_pred2)

print (classification_report (y_test, y_pred2))

"""## Over Sampling"""

!pip install smote-variants

print("Before OverSampling count of yes: {}".format(sum(y_train==1)))
print("Before OverSampling count of no: {} \n".format(sum(y_train==0)))

import smote_variants as sv

# Instantiating the SMOTE class
oversampler= sv.SMOTE()

# Creating new training set

X_train_us, y_train_us = oversampler.sample(np.array(X_train), np.array(y_train))

# Shape after oversampling

print('After OverSampling, the shape of train_X: {}'.format(X_train_us.shape))
print('After OverSampling, the shape of train_y: {} \n'.format(y_train_us.shape))

print("After OverSampling, counts of label 'Yes': {}".format(sum(y_train_us==1)))
print("After OverSampling, counts of label 'no': {}".format(sum(y_train_us==0)))

# Defining New Model
xgb_os = XGBClassifier()
xgb_os.fit(X_train_us, y_train_us)

y_pred3 = xgb_os.predict(np.array(X_test))

"""### Results:"""

confusion_matrix(y_test, y_pred3)

print (classification_report (y_test, y_pred3))

"""## MSMOTE"""

# Instantiating the SMOTE class
oversampler= sv.MSMOTE()
# Creating new training sts
X_train_ms, y_train_ms = oversampler.sample(np.array(X_train), np.array(y_train))

# Shape after MSMOTE
print('After MSMOTE, the shape of train_X: {}'.format(X_train_ms.shape))
print('After MSMOTE, the shape of train_y: {} \n'.format(y_train_ms.shape))

xgb_ms =  XGBClassifier()
xgb_ms.fit(X_train_ms, y_train_ms)

y_pred4 = xgb_ms.predict(np.array(X_test))

"""### Results:"""

confusion_matrix(y_test, y_pred4)

print (classification_report (y_test, y_pred4))

"""## Thoughts:
We are going to tune this model even further.  Our goal is to get the highest recall for our yes class as possible, without sacrificing too much precision.  It looks like using the undersampled training set is the way to do this.

## Tuning (Baseline)
With the undersampled training data, we set the parameters to commonly used values to be a baseline.  We will tune as many as possible.
"""

xgb1 = XGBClassifier(
 learning_rate =0.1,
 n_estimators=500,
 max_depth=4,
 min_child_weight=1,
 gamma=0,
 subsample=0.8,
 colsample_bytree=0.8,
 objective= 'binary:logistic',
 nthread=4,
 scale_pos_weight=1,
 seed=27)

xgb1.fit(X_trainNew, y_trainNew)

y_pred_x1 = xgb1.predict(X_test)

"""### Results:"""

confusion_matrix(y_test, y_pred_x1)

print (classification_report (y_test, y_pred_x1))

"""## Tuning (maxdepth and minchildweight)"""

from sklearn.metrics import f1_score
f1_scorer = make_scorer(f1_score, pos_label=1)

from sklearn.model_selection import GridSearchCV

param_test2 = {
 'max_depth':[1,2,3,4,5],
 'min_child_weight':[1,2,3,4,5]
}
gsearch2 = GridSearchCV(estimator = XGBClassifier( learning_rate=0.1, n_estimators=500, max_depth=5,
 min_child_weight=2, gamma=0, subsample=0.8, colsample_bytree=0.8,
 objective= 'binary:logistic', nthread=4, scale_pos_weight=1,seed=27), 
 param_grid = param_test2, scoring=recall_scorer,n_jobs=4,cv=5)

gsearch2.fit(X_trainNew,y_trainNew)

gsearch2.best_params_, gsearch2.best_score_

xgb2 = XGBClassifier(
 learning_rate =0.1,
 n_estimators=500,
 max_depth=4,
 min_child_weight=4,
 gamma=0,
 subsample=0.8,
 colsample_bytree=0.8,
 objective= 'binary:logistic',
 nthread=4,
 scale_pos_weight=1,
 seed=27)

xgb2.fit(X_trainNew, y_trainNew)

y_pred_x2 = xgb2.predict(X_test)

"""### Results:"""

confusion_matrix(y_test, y_pred_x2)

print (classification_report (y_test, y_pred_x2))

"""## Tuning (Gamma)"""

param_test3 = {
 'gamma':[i/10.0 for i in range(0,5)]
}

gsearch3 = GridSearchCV(estimator = XGBClassifier( learning_rate =0.1, n_estimators=500, max_depth=4,
 min_child_weight=4, gamma=0, subsample=0.8, colsample_bytree=0.8,
 objective= 'binary:logistic', nthread=4, scale_pos_weight=1,seed=27), 
 param_grid = param_test3, scoring=recall_scorer,n_jobs=4,cv=5)

gsearch3.fit(X_trainNew, y_trainNew)

gsearch3.best_params_, gsearch3.best_score_

xgb3 = XGBClassifier(
 learning_rate =0.1,
 n_estimators=500,
 max_depth=4,
 min_child_weight=4,
 gamma=0.0,
 subsample=0.8,
 colsample_bytree=0.8,
 objective= 'binary:logistic',
 nthread=4,
 scale_pos_weight=1,
 seed=27)

xgb3.fit(X_trainNew, y_trainNew)

y_pred_x3 = xgb3.predict(X_test)

"""### Results:"""

confusion_matrix(y_test, y_pred_x3)

print (classification_report (y_test, y_pred_x3))

"""## Tuning (subsample and colsample_bytree)"""

param_test4 = {
 'subsample':[i/10.0 for i in range(6,10)],
 'colsample_bytree':[i/10.0 for i in range(6,10)]
}

gsearch4 = GridSearchCV(estimator = XGBClassifier( learning_rate =0.1, n_estimators=500, max_depth=4,
 min_child_weight=4, gamma=0, subsample=0.8, colsample_bytree=0.8,
 objective= 'binary:logistic', nthread=4, scale_pos_weight=1,seed=27), 
 param_grid = param_test4, scoring=recall_scorer,n_jobs=4,cv=5)

gsearch4.fit(X_trainNew, y_trainNew)

gsearch4.best_params_ , gsearch4.best_score_

param_test5 = {
 'subsample':[i/100.0 for i in range(75,90,5)],
 'colsample_bytree':[i/100.0 for i in range(75,90,5)]
}

gsearch5 = GridSearchCV(estimator = XGBClassifier( learning_rate =0.1, n_estimators=500, max_depth=4,
 min_child_weight=4, gamma=0, subsample=0.9, colsample_bytree=0.6,
 objective= 'binary:logistic', nthread=4, scale_pos_weight=1,seed=27), 
 param_grid = param_test5, scoring=recall_scorer,n_jobs=4,cv=5)

gsearch5.fit(X_trainNew, y_trainNew)

gsearch5.best_params_ , gsearch5.best_score_

xgb5 = XGBClassifier(
 learning_rate =0.1,
 n_estimators=500,
 max_depth=4,
 min_child_weight=4,
 gamma=0,
 subsample=0.8,
 colsample_bytree=0.8,
 objective= 'binary:logistic',
 nthread=4,
 scale_pos_weight=1,
 seed=27)

xgb5.fit(X_trainNew, y_trainNew)

y_pred_x5 = xgb5.predict(X_test)

"""### Results:"""

confusion_matrix(y_test, y_pred_x5)

print (classification_report (y_test, y_pred_x5))

"""## Tuning (Regularization Parameters)"""

param_test6 = {
 'reg_alpha':[1e-5, 1e-2, 0.1, 1, 100]
}
gsearch6 = GridSearchCV(estimator = XGBClassifier( learning_rate =0.1, n_estimators=500, max_depth=4,
 min_child_weight=4, gamma=0.4, subsample=0.8, colsample_bytree=0.8,
 objective= 'binary:logistic', nthread=4, scale_pos_weight=1,seed=27), 
 param_grid = param_test6, scoring=recall_scorer,n_jobs=4,cv=5)

gsearch6.fit(X_trainNew, y_trainNew)

gsearch6.best_params_,gsearch6.best_score_

xgb6 = XGBClassifier(
 learning_rate =0.1,
 n_estimators=500,
 max_depth=4,
 min_child_weight=4,
 gamma=0,
 subsample=0.8,
 colsample_bytree=0.8,
 reg_alpha= .0001,
 objective= 'binary:logistic',
 nthread=4,
 scale_pos_weight=1,
 seed=27)

xgb6.fit(X_trainNew, y_trainNew)

y_pred_x6 = xgb6.predict(X_test)

"""### Results:"""

confusion_matrix(y_test, y_pred_x6)

print (classification_report (y_test, y_pred_x6))

"""## Tuning (Lowering Learning Rate)"""

param_test7 = {
 'learning_rate':[.01,.03,.05,.1]
}
gsearch7 = GridSearchCV(estimator = XGBClassifier( learning_rate =0.1, n_estimators=500, max_depth=4,
 min_child_weight=4, gamma=0, subsample=0.8, colsample_bytree=0.8,
 objective= 'binary:logistic', nthread=4, scale_pos_weight=1,seed=27), 
 param_grid = param_test7, scoring=recall_scorer,n_jobs=4,cv=5)

gsearch7.fit(X_trainNew, y_trainNew)

gsearch7.best_params_,gsearch6.best_score_

xgb7 = XGBClassifier(
 learning_rate =0.01,
 n_estimators=500,
 max_depth=3,
 min_child_weight=4,
 gamma=0,
 subsample=0.9,
 colsample_bytree=0.9,
 objective= 'binary:logistic',
 nthread=4,
 scale_pos_weight=1,
 seed=27)

xgb7.fit(X_trainNew, y_trainNew)

y_pred_x7 = xgb7.predict(X_test)

"""### Results:"""

confusion_matrix(y_test, y_pred_x7)

print (classification_report (y_test, y_pred_x7))

"""## Final Thoughts on XGBoost
- Baseline

|Class||Precision||Recall||F1-Score|
|-----||---------||------||--------|
|Yes||0.75||0.20||0.32 |

- After Undersampling

|Class||Precision||Recall||F1-Score|
|-----||---------||------||--------|
|Yes||0.17||0.89||0.29 |

- After All That Tuning!

|Class||Precision||Recall||F1-Score|
|-----||---------||------||--------|
|Yes||0.18||0.91||0.30 |

<br>

1. Undersampling made the biggest difference.
2. Tuning was able to both improve precision and recall, but only slightly.
3. If we wanted to focus more on precision and f1-score, we could have tuned the over-sampled model.
4. Precision was definitely sacrificed for recall.
5. If we had chosen to use the over-sampled data, the run times for fitting the models while tuning would have been extremely long.
5. In the end our model caught all but 4 companies from our test data that went bankrupt. Our final recall was 91%.

# PCA

Examining if Principle Component Analysis
"""

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

pca_X = df_X.copy()

# In order for PCA to work correctly, any categorical variables need to be removed

pca_X.drop(labels=[94], axis=1, inplace = True)

pca_X.head(1)

X_train_pca, X_test_pca, y_train_pca, y_test_pca = train_test_split(pca_X, df_y, test_size=0.20, random_state=1, stratify= df_y)

print(y_train_pca.value_counts('Yes'))
print(y_test_pca.value_counts('Yes'))

"""Getting scree plot"""

from sklearn.decomposition import PCA

#define PCA model to use
pca1 = PCA(.95)

#fit PCA model to data
pca_fit = pca1.fit(df_X)

import matplotlib.pyplot as plt
import numpy as np

PC_values = np.arange(pca1.n_components_) + 1
plt.plot(PC_values, pca.explained_variance_ratio_, 'o-', linewidth=2, color='blue')
plt.title('Scree Plot')
plt.xlabel('Principal Component')
plt.ylabel('Variance Explained')
plt.show()

print(pca1.explained_variance_ratio_)

"""Using PCA to compare algorithm outputs"""

from sklearn.metrics import accuracy_score, log_loss
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier

results_pca = []
names_pca = []

modelsPCA = []
modelsPCA.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
modelsPCA.append(('LDA', LinearDiscriminantAnalysis()))
modelsPCA.append(('KNN', KNeighborsClassifier()))
modelsPCA.append(('CART', DecisionTreeClassifier()))
modelsPCA.append(('NB', GaussianNB()))
modelsPCA.append(('SVM', SVC(gamma='auto')))
modelsPCA.append(('XGB', XGBClassifier()))
modelsPCA.append(('RFC', RandomForestClassifier()))
    
#for classifier in classifiers:
for name, model in modelsPCA:
  pipe = Pipeline(steps=[('scaler', StandardScaler()), ('pca', PCA(n_components=.95)), ('classifier', model)])
  kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
  cv_results = cross_val_score(pipe, X_train_pca, y_train_pca, cv=kfold, scoring='accuracy')
  results_pca.append(cv_results)
  names_pca.append(name)
  print('%s: %f accuracy    (%f) std' % (name, cv_results.mean(), cv_results.std()))

# Listing recall by model instead of just accurcy above

for name, model in modelsPCA:
  pipe = Pipeline(steps=[('scaler', StandardScaler()), ('pca', PCA(n_components=.95)), ('classifier', model)])
  kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
  cv_results = cross_val_score(pipe, X_train_pca, y_train_pca, cv=kfold, scoring='recall')
  results_pca.append(cv_results)
  names_pca.append(name)
  print('%s: %f recall    (%f) std' % (name, cv_results.mean(), cv_results.std()))

for name, model in modelsPCA:
  pipe = Pipeline(steps=[('scaler', StandardScaler()), ('pca', PCA(n_components=.95)), ('classifier', model)])
  kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
  cv_results = cross_val_score(pipe, X_train_pca, y_train_pca, cv=kfold, scoring='f1')
  results_pca.append(cv_results)
  names_pca.append(name)
  print('%s: %f f1    (%f) std' % (name, cv_results.mean(), cv_results.std()))

for name, model in modelsPCA:
  pipe = Pipeline(steps=[('scaler', StandardScaler()), ('pca', PCA(n_components=.95)), ('classifier', model)])
  pipe.fit(X_train_pca, y_train_pca)
  pred = pipe.predict(X_test_pca)
  print(confusion_matrix(y_test_pca, pred))
  print(classification_report(y_test_pca, pred))

"""# SMOTE plus PCA"""

print("Before OverSampling count of Bankrupt: {}".format(sum(y_train_pca ==1)))
print("Before OverSampling count of not Bankrupt: {} \n".format(sum(y_train_pca ==0)))

import smote_variants as sv

# Instantiating the SMOTE class
oversampler= sv.SMOTE()

X_train_ov_pca, y_train_ov_pca = oversampler.sample(np.array(X_train_pca), np.array(y_train_pca))

# Shape after oversampling

print('After OverSampling, the shape of train_X: {}'.format(X_train_ov_pca.shape))
print('After OverSampling, the shape of train_y: {} \n'.format(y_train_ov_pca.shape))

print("After OverSampling, counts of label 'Yes': {}".format(sum(y_train_ov_pca==1)))
print("After OverSampling, counts of label 'no': {}".format(sum(y_train_ov_pca==0)))

for name, model in modelsPCA:
  pipe = Pipeline(steps=[('scaler', StandardScaler()), ('pca', PCA(n_components=.95)), ('classifier', model)])
  kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
  cv_results = cross_val_score(pipe, X_train_ov_pca, y_train_ov_pca, cv=kfold, scoring='accuracy')
  results_pca.append(cv_results)
  names_pca.append(name)
  print('%s: %f accuracy   (%f) std' % (name, cv_results.mean(), cv_results.std()))

for name, model in modelsPCA:
  pipe = Pipeline(steps=[('scaler', StandardScaler()), ('pca', PCA(n_components=.95)), ('classifier', model)])
  kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
  cv_results = cross_val_score(pipe, X_train_ov_pca, y_train_ov_pca, cv=kfold, scoring='precision')
  results_pca.append(cv_results)
  names_pca.append(name)
  print('%s: %f precision   (%f) std' % (name, cv_results.mean(), cv_results.std()))

for name, model in modelsPCA:
  pipe = Pipeline(steps=[('scaler', StandardScaler()), ('pca', PCA(n_components=.95)), ('classifier', model)])
  kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
  cv_results = cross_val_score(pipe, X_train_ov_pca, y_train_ov_pca, cv=kfold, scoring='recall')
  results_pca.append(cv_results)
  names_pca.append(name)
  print('%s: %f recall   (%f) std' % (name, cv_results.mean(), cv_results.std()))

for name, model in modelsPCA:
  pipe = Pipeline(steps=[('scaler', StandardScaler()), ('pca', PCA(n_components=.95)), ('classifier', model)])
  kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
  cv_results = cross_val_score(pipe, X_train_ov_pca, y_train_ov_pca, cv=kfold, scoring='f1')
  results_pca.append(cv_results)
  names_pca.append(name)
  print('%s: %f f1   (%f) std' % (name, cv_results.mean(), cv_results.std()))