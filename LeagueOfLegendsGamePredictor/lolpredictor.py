# -*- coding: utf-8 -*-
"""LolPredictor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1idCN6KX7s4E-IyhQmU27jIbgMTyRVZTV

# League of Legends Game Outcome Predictor
This is work done by Frank Rodriguez and Michael Seman to create a model to predict the outcome of a League of Legends game based on the team stats at 10 minutes.

Link - https://www.kaggle.com/datasets/bobbyscience/league-of-legends-diamond-ranked-games-10-min

## Goal:
Our goal is to train a binary classification ML model to accurately predict the winner of a league of legends game, given the team stats at the 10 minute mark of the game.  blueWins is our target variable.  0 means a red win, 1 means a blue win.
"""

# loading basic libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# loading dataset
df = pd.read_csv('https://raw.githubusercontent.com/michaelseman/mydatasets/main/high_diamond_ranked_10min.csv')
# allowing all columns to be viewed.
pd.set_option('max_columns',None)
pd.set_option('max_rows',None)

"""# Preliminary EDA"""

# Looking at the first 5 records of the dataframe

df.head()

# our target column is blueWins

# Inspecting dataset and looking for nulls and check data types

df.info()

# After examining the data, we see many redundant/100% correlated columns columns because of how the data was recorded.  
# These will be removed later in data cleaning.

df.columns

# Dropping the gameId column 
df = df.drop(columns=['gameId'], axis=1)

# Looking at Meta information for dataset
df.describe().T

df.nunique()

"""Note: Although the previous line of code shows what could be quite a few categorical columns, the timeframe in which the match statistics
were taken, turns variables that are continuous, but discrete and makes them look like something categorical. Examples of this would be red/blue Dragons as they spawn at 5:00 into the match and once killed it respawns every 5:00 so there is not really a chance to get more than one kill in 10 minutes.
"""

# Just checking on some possible categorical variables

print('blueFirstBlood ' + str(sorted(df['blueFirstBlood'].unique())))

print('redFirstBlood ' + str(sorted(df['redFirstBlood'].unique())))

print('redTowersDestroyed ' + str(sorted(df['redTowersDestroyed'].unique())))

# The towers destroyed column is another one of those variables that may look like a categorical variable, but the time limit and the fact that
# there are only 9 towers in total explain this fact well

print('blueTowersDestroyed ' + str(sorted(df['blueTowersDestroyed'].unique())))

# Double Checking for Null Values 
df.isnull().sum()

# Checking for target variable imbalance
df['blueWins'].value_counts()

df['blueWins'].value_counts(normalize=True)

"""## Univariate Visualizations"""

# Visually checking target variable "imbalance" 

sns.countplot(x='blueWins', data = df)
plt.title('blueWins distribution')

# exploring this column specifically for distribution of values
df['blueWardsPlaced'].nunique()
df['blueWardsPlaced'].unique()
pd.set_option('max_rows',90)

df['blueWardsPlaced'].value_counts()

pd.set_option('max_rows',30)

"""# Initial Data Cleaning/Feature Selection
This section requires a bit of knowledge about the PC game League of Legends.  A lot of these columns are measuring the same exact thing and essentially just add clutter to the dataframe.  So we are going to remove that clutter now, before moving forward with more EDA.

Let's look at our columns:
- target = 'blueWins',

- dont need = 'gameId', 'blueEliteMonsters','redEliteMonsters',
- exist in another form = 'blueTotalGold', 'blueTotalExperience','blueCSPerMin', 'blueGoldPerMin', 'blueAvgLevel',
'redTotalGold', 'redTotalExperience','redCSPerMin', 'redGoldPerMin,'redAvgLevel',

- redundant = 'redGoldDiff','redExperienceDiff', 'redFirstBlood','redKills', 'redDeaths', 

- keepers = 'blueWardsPlaced', 'blueWardsDestroyed','blueFirstBlood', 'blueKills', 'blueDeaths', 'blueAssists', 'blueDragons', 'blueHeralds','blueTowersDestroyed',   'blueTotalMinionsKilled',
'blueTotalJungleMinionsKilled', 'blueGoldDiff', 'blueExperienceDiff',
'redWardsPlaced', 'redWardsDestroyed','redAssists', 'redDragons', 'redHeralds', 'redTowersDestroyed', 'redTotalMinionsKilled', 'redTotalJungleMinionsKilled',

Explanations:

- The EliteMonsters column for both red and blue teams is just a total number of herald and dragon kills, we can remove both of these as we already have individual columns for each. We would rather track each variable separately as the dragon and herald work slightly different.
</br>
</br>
- We chose to evaluate the amount of gold for each team using one column - blueGoldDiff (which is the difference in each teams Gold count from the blue team's perpective, so negative values mean that the red team has that much more gold).  As a result we can remove the columns for TotalGold and GoldPerMin for both teams.
</br>
</br>
- We chose to evaluate experience with one column - blueExpDiff (which is the difference in each teams amount of experience points (EXP) from the blue teams perpective).  As a results we can eliminate TotalExperience, and AvgLevel. *Note* Levels are determined by the amount of experience points gained by each team member, so ExpDiff is essentially measuring the same metric as AvgLevel, which means they would be highly correlated with each other and we to eliminate as many of those types of variables as possible
</br>
</br>
- The same statistics exist for both teams. As a result, there are some values for one team that are essentially the inverse of another column for the other team. One example of this would be the fact that the value for blueKills (amount of times the blue team killed a member of the red team) would be the same value as redDeaths (amount of times the red team was killed by an opponent from the blue team). We chose to keep the blue team's version of those values. Other red team columns that we eliminated for the same reason: GoldDiff, ExperienceDiff, FirstBlood, Kills, and Deaths. *Note*: In League of Legends, FirstBlood (aka the first kill of the game) can only be achieved by one team.  So blueFirstBlood 1 means blue got the first kill, 0 means red got the first kill.
"""

# Eliminating all the columns mentioned above in the sections: 'don't need', 'exist in another form', & 'redundant'

df = df.drop(columns=['blueTotalGold', 'blueTotalExperience', 'redFirstBlood','blueAvgLevel','redAvgLevel','blueCSPerMin',  'redKills','redDeaths', 'blueGoldPerMin','blueEliteMonsters','redEliteMonsters','redTotalExperience','redTotalGold','redGoldDiff','redExperienceDiff','redCSPerMin', 'redGoldPerMin'],  axis=1)

# Checking columns left over after removing the columns in the code section above

df.columns

# Examining the first 5 values of the most updated dataframe

df.head()

"""# EDA cont.

## Univariate Visualizations cont.
"""

# Using Box-Whisker Plots to identify outliers for each column

for column in range(1,len(df.columns)):
   plt.figure(figsize=(5,3))
   sns.boxplot(x=df.iloc[column])
   plt.title(f'Boxplot for {df.columns[column]}')
   plt.show()

"""## Bivariate Visualizations"""

# Showing the percentage of first blood sucess and failure and seeing its effects on winning or losing a match

pd.crosstab(df.blueWins, df.blueFirstBlood, normalize='index').plot.bar()

# Showing the percentage of dragon kills for each team and showing its effect on winning the match
#

pd.crosstab(df.blueWins, df.blueDragons, normalize='index').plot.bar()
pd.crosstab(df.blueWins, df.redDragons, normalize='index').plot.bar()

print(df.blueDragons.value_counts())
print(df.redDragons.value_counts())

# graphing heralds for each side, red/blue and how it breaks down with blue side winning. If it is even on both sides, the graphs should look the same but left and right swapped.
# It also shows how in these matches, whether a team killed the herald monster or not, 
# it did not have much of an effect on the outcome of match itself and we will see this later show up again as well

pd.crosstab(df.blueWins, df.blueHeralds, normalize='index').plot.bar(stacked=True)
pd.crosstab(df.blueWins, df.redHeralds, normalize='index').plot.bar(stacked=True)

# herald seems to slightly favor 

# Look like the blue team got slightly more heralds throughout all the matches, 
# but again the graphs above show how it does not seem to have much of an effect on the match outcome 
print(df.blueHeralds.value_counts())
print(df.redHeralds.value_counts())

"""## Multivariate Visualizations"""

df.corr()

plt.figure(figsize=(15, 15)) # old cmap value RdYlGn
sns.heatmap(df.corr(), annot=True, cmap="rainbow", annot_kws={"size":8})

!pip install hvplot
import hvplot.pandas

hvplot.extension('bokeh')
df.drop('blueWins', axis=1).corrwith(df.blueWins).hvplot.barh()

"""### Correlation Conclusions
- With respect to wins: The predictors with the highest correlation to wins in order are: GoldDiff, ExpDiff, Deaths/Kills, Assists, TotalMinionsKilled, Dragons.

- Gold is slighty more important that Experience point for winning

- It is not explicitly a zero sum gain with Dragons and Heralds.  There is only 1 of each monster available to be fight and then use before 10 minutes. With that in mind, if one team kills one, it will not appear again within the 10-minute time frame our data shows. However, there is a possibility that neither team will be able to take either objective.

- Assists require Kills to happen, but a kill can result in multiple or no assists.

- Placing wards seems to be the least correlated factor with wins

# Data Cleaning cont.
"""

# Checking for duplicates
df.duplicated().sum()

"""## Checking Distribution / Outlier Removal"""

# Investigating Distributions of Variables
df.hist(bins=25, figsize=(15, 25), layout=(-1, 5), edgecolor="black")
plt.tight_layout();

# There are curious values in terms of wards placed
# you are able to place 1 ward every 90 seconds, you can also buy additional wards for 75g.
# remember there are 5 players per team that are all able to place wards

# If 90 sec thing is true 
# Just using time as a limiting factor, the most amount of wards that can be placed 
# on the field by a whole team in 10 minutes is 33.

# Looking at the average amount of wards placed

np.mean(df['blueWardsPlaced'])

# graphing distribution of wards placed
from matplotlib import rcParams
rcParams['figure.figsize'] = (16, 6)
rcParams['axes.spines.top'] = False
rcParams['axes.spines.right'] = False

plt.hist(df['blueWardsPlaced'], bins=100);
plt.hist(df['redWardsPlaced'], bins=100);

# at the max value we see players placing 50 wards over the course of 10 mins, so 5 wards per minute.
# there may be a way for this to be possible, but this is definitely not optimal play
# something in is going on in this games w super high ward placement numbers
max(df['blueWardsPlaced'])/5

# Just checking the correlation between wards placed by one team and destroyed by the other

df['blueWardsPlaced'].corr(df['redWardsDestroyed'])

# How many records include values that are 3 times higher than the mean
sum(df['blueWardsPlaced']>(3*np.mean(df['blueWardsPlaced'])))

# getting z scores
from scipy import stats
df['ward_z'] = np.abs(stats.zscore(df['blueWardsPlaced']))
df['redward_z'] = np.abs(stats.zscore(df['redWardsPlaced']))

# examining values of higher z scores
print(sum(df['ward_z']>4))
df[df['ward_z']>8]

# examining values of higher z scores
print(sum(df['redward_z']>4))
df[df['redward_z']>8]

df.shape

df['kill_z'] = np.abs(stats.zscore(df['blueKills']))

print(sum(df['kill_z']>4))
df[df['kill_z']>4]

pd.set_option('max_rows',30)

df.shape

df.columns

# dropping the newly created z score columns
df = df.drop(columns=['ward_z','redward_z','kill_z'], axis=1)

df.shape

sum(df['redTowersDestroyed'])

sum(df['blueTowersDestroyed'])

# df1 = df1.loc[df1['redward_z'] <= 4] 
# np.abs(stats.zscore(df['blueWardsPlaced']))
# df[np.abs(stats.zscore(df.iloc[:,1])) <= 4]
# df = df[np.abs(stats.zscore(df.iloc[:,column])) <= 4]
# len(df.columns)

df['blueWins'].nunique()

# Removing outliers
# this loop goes through every column and computes the z score of each record
# it then drops every record where the z score is over 4 and prints the resulting shape
for column in df.columns:
  if df[column].nunique() > 5:
    df = df[np.abs(stats.zscore(df[column])) <= 4]
  print(column,df.shape)

# shape after removing outliers
df.shape

"""## Feature Relationships: Looking at Multi-Colinearity"""

sns.set(style="white")
corr = df.corr()
mask = np.zeros_like(corr, dtype=bool)
mask[np.triu_indices_from(mask)] = True
f, ax = plt.subplots(figsize=(11,9))
cmap = sns.diverging_palette(220,10,as_cmap=True)
sns.heatmap(corr,mask=mask,cmap=cmap,vmax=1,center=0,square=True, 
            linewidth=.5, cbar_kws={'shrink': .5}, annot=True,annot_kws={"size":7})
ax.set_title('Multi-Collinearity of Features')

"""Three columns stand out.  Blue and Reds Assists and Experience Diff.
</br>
Given the high values for their correlations to other non target columns, we will be removing them.
</br>

"""

# saving a copy of the dataframe with assists and expdiff, just in case we want to revisit later
df1 = df
df1.head(2)

# Dropped the assists because of the multi-collinearity wtih blueKills and blueDeaths
# and blueExpDiff because of the multi-collinearity with blueGoldDiff


df = df.drop(columns=['blueAssists', 'redAssists', 'blueExperienceDiff'],axis=1)

df.head(2)

df.shape

"""## Encoding Categorical Data:

With the feature selection we made earlier we eliminated most of the categorical variables. In the most recent dataframe we only have blueFirstBlood and it was already in our dataset as a one hot encoded value.

# Creating a Model

## Splitting the Data
"""

# df.iloc[:,1:]
# df.iloc[:,0]

X,Y = df.iloc[:,1:], df.iloc[:,0]

# splitting data 80/20
from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(df.iloc[:,1:], df.iloc[:,0], test_size=0.2, random_state=22)
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=22)

"""## Algorithm Harness"""

!pip install catboost

# Compare Algorithms
from sklearn.metrics import roc_auc_score
from time import time
from sklearn.metrics import explained_variance_score,mean_absolute_error,r2_score
from pandas import read_csv
from matplotlib import pyplot
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from sklearn.ensemble import AdaBoostClassifier
from lightgbm import LGBMClassifier

models = []
models.append(('LR', LogisticRegression(solver='liblinear')))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('RF', RandomForestClassifier()))
models.append(('XGB', XGBClassifier()))
models.append(('CAT', CatBoostClassifier(verbose=0)))
models.append(('ADA', AdaBoostClassifier()))
models.append(('LGBM',LGBMClassifier()))

# evaluate each model in turn
results = []
names = []
scoring = 'accuracy'
for name, model in models:
    start = time()
    kfold = KFold(n_splits=10, random_state=7, shuffle=True)
    model.fit(X_train, y_train)
    train_time = time() - start
    cv_results = cross_val_score(model, X_train, y_train, cv=kfold, scoring=scoring)
    predict_time = time()-start 
    results.append(cv_results)
    names.append(name)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    #y_pred = model.predict_proba(X_train)[:, 1]
    #auc = roc_auc_score(y_train, y_pred)
    print(msg)
    print("Score for each of the 10 K-fold tests: ",cv_results)
    print(model)
    print("\tTraining time: %0.3fs" % train_time)
    print("\tPrediction time: %0.3fs" % predict_time)
    #y_pred = model.predict(X_test)
    #print("\tExplained variance:", explained_variance_score(y_test, y_pred))
    print()
    
    
    
# boxplot algorithm comparison
fig = pyplot.figure()
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
pyplot.boxplot(results)
ax.set_xticklabels(names)
pyplot.show()

"""## Most Important Features Per XGBoost"""

xgb_clf = XGBClassifier()
xgb_clf.fit(X_train, y_train)

def feature_imp(df, model):
    fi = pd.DataFrame()
    fi["feature"] = df.columns
    fi["importance"] = model.feature_importances_
    return fi.sort_values(by="importance", ascending=False)

df_features = feature_imp(X, xgb_clf)
df_features.set_index('feature', inplace=True)
df_features.plot(kind='barh', figsize=(10, 8))
plt.title('Feature Importance according to XGBoost')

"""# XGBoost
attempting Bayesian Optimization for XGBoost
"""

!pip install bayesian-optimization

"""## Baseline Model"""

df.head()

df2 = df1.drop(columns=['blueAssists', 'redAssists'],axis=1)

# splitting data 80/20
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(df.iloc[:,1:], df.iloc[:,0], test_size=0.2, random_state=22)

import xgboost as xgb
from xgboost import XGBClassifier
from bayes_opt import BayesianOptimization
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score

from sklearn.metrics import roc_auc_score, recall_score

xgb_clf = XGBClassifier()
xgb_clf.fit(X_train, y_train)

"""### Results:"""

predictions_xgb = xgb_clf.predict(X_test)
confusion_matrix(y_test, predictions_xgb)

# high_score = 725+662 - disregard
accuracy_score(y_test, predictions_xgb)

print(classification_report(y_test, predictions_xgb))

# creating a dictionary to store scores of our models, pre and post tuning
dict_scores = {}
dict_scores[0] = {'Model': 'XGBoost', 'State': 'Pre-tuning', 'Accuracy': round(accuracy_score(y_test, predictions_xgb),4), 'AUC':round(roc_auc_score(y_test, predictions_xgb),4), 'Blue Win Accuracy':round(recall_score(predictions_xgb, y_test, pos_label=1),4), 'Red Win Accuracy':round(recall_score(predictions_xgb, y_test, pos_label=0),4)}
dict_scores

"""## Tuning Hyperparameters using Bayesian Optimization"""

# https://analyticsindiamag.com/implementing-bayesian-optimization-on-xgboost-a-beginners-guide/

#Converting the dataframe into XGBoost’s Dmatrix object
dtrain = xgb.DMatrix(X_train, label=y_train)

#Bayesian Optimization function for xgboost
#specify the parameters you want to tune as keyword arguments
def bo_tune_xgb(max_depth, gamma, n_estimators ,learning_rate, min_child_weight):
  params = {'max_depth': int(max_depth),
              'gamma': gamma,
              'n_estimators': int(n_estimators),
              'learning_rate':learning_rate,
              'min_child_weight':min_child_weight,
              'subsample': .8,
              'eta': 0.1,
              'eval_metric': 'error'}
  cv_result = xgb.cv(params, dtrain, num_boost_round=70, nfold=10)
    #Return the negative error
  return -1.0 * cv_result['test-error-mean'].iloc[-1]

#Invoking the Bayesian Optimizer with the specified parameters to tune
xgb_bo = BayesianOptimization(bo_tune_xgb, {'max_depth': (3, 10),
                                             'gamma': (0, 1),
                                             'learning_rate':(0,1),
                                             'n_estimators':(100,120),
                                             'min_child_weight':[1,5],
                                            })

#performing Bayesian optimization for 5 iterations with 8 steps of random exploration with an #acquisition function of expected improvement
xgb_bo.maximize(n_iter=6, init_points=8, acq='ei')

#Extracting the best parameters
params = xgb_bo.max['params']
print(params)

#Converting the max_depth and n_estimator values from float to int
params['max_depth']= int(params['max_depth'])
params['n_estimators']= int(params['n_estimators'])

#Initialize an XGBClassifier with the tuned parameters and fit the training data
classifier2 = XGBClassifier(**params).fit(X_train, y_train)

"""### Results:"""

predictions_xgb2 = classifier2.predict(X_test)
print(classification_report(y_test, predictions_xgb2))

confusion_matrix(y_test, predictions_xgb2)

# storing scores in a dictionary
dict_scores[1] = {'Model': 'XGBoost', 'State': 'Post-tuning', 'Accuracy': round(accuracy_score(y_test, predictions_xgb2),4), 'AUC':round(roc_auc_score(y_test, predictions_xgb2),4), 'Blue Win Accuracy':round(recall_score(predictions_xgb2, y_test, pos_label=1),4), 'Red Win Accuracy':round(recall_score(predictions_xgb2, y_test, pos_label=0),4)}
dict_scores

# disregard, for personal use
high_score2 = (721+661)
706+663

"""## Tuning Hyperparameters using GridSearch"""

from sklearn.model_selection import GridSearchCV

estimators = np.arange(100,200,5)
depth = np.arange(1,11,1)
param_test = {
 'n_estimators':estimators,
 'max_depth':depth,
 'min_child_weight':[1,2,3,4,5],
 'gamma':[i/10.0 for i in range(0,5)],
 'subsample':[i/10.0 for i in range(6,10)],
 'colsample_bytree':[i/10.0 for i in range(6,10)],
 'reg_alpha':[1e-5, 1e-2, 0.1, 1, 100]
}

params

param_test = {
    'subsample':[i/10.0 for i in range(6,10)],
    'colsample_bytree':[i/10.0 for i in range(6,10)]
}
gsearch = GridSearchCV(estimator = XGBClassifier( learning_rate=0.02822659452140064, n_estimators=118, max_depth=4,
 min_child_weight=3, gamma=0.5831229908326606, subsample=0.8, colsample_bytree=0.8,
 objective= 'binary:logistic', nthread=4, scale_pos_weight=1,seed=27), 
 param_grid = param_test, scoring='accuracy',n_jobs=4,cv=5)

gsearch.fit(X_train, y_train)

gsearch.best_params_, gsearch.best_score_

param_test2 = {
 'subsample':[i/100.0 for i in range(65,80,5)],
 'colsample_bytree':[i/100.0 for i in range(75,90,5)]
}
gsearch2 = GridSearchCV(estimator = XGBClassifier( learning_rate=0.02822659452140064, n_estimators=118, max_depth=4,
 min_child_weight=3, gamma=0.5831229908326606, subsample=0.8, colsample_bytree=0.8,
 objective= 'binary:logistic', nthread=4, scale_pos_weight=1,seed=27), 
 param_grid = param_test, scoring='accuracy',n_jobs=4,cv=5)

gsearch2.fit(X_train, y_train)

gsearch2.best_params_, gsearch.best_score_

params

xgb1 = XGBClassifier(
 learning_rate =0.02822659452140064,
 n_estimators=118,
 max_depth=4,
 min_child_weight=3.4208225590655257,
 gamma=0.5831229908326606,
 subsample=0.8,
 colsample_bytree=0.8,
 objective= 'binary:logistic',
 nthread=4,
 scale_pos_weight=1,
 seed=27)

xgb1.fit(X_train, y_train)

y_pred = xgb1.predict(X_test)

confusion_matrix(y_test, y_pred)

print (classification_report (y_test, y_pred))

"""### Note:
This section was done as more of a personal curiousity to see if I could get similar/better results than I did with Bayesian Optimization.  And also as a means to make sure I implemented Bayesian Optimization properly.  My conclusions were that, tuning using gridsearch took a lot longer and was producing worse results.

# Logistic Regression
"""

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import sklearn

pipeline_lr = make_pipeline(StandardScaler(), LogisticRegression(max_iter=5000))

hyperparam_grid = {
    'logisticregression__solver': ['newton-cg', 'lbfgs', 'liblinear'],
    'logisticregression__penalty': ['l2'],
    'logisticregression__C' : [100, 10, 1.0, 0.1, 0.01]
}

pipe_grid_lr = GridSearchCV(pipeline_lr, param_grid=hyperparam_grid, cv=10, scoring='f1')

LogisticRegression().get_params().keys()

pipe_grid_lr.fit(X_train, y_train)

pipe_grid_lr.best_params_

pipeline_lr_tuned = make_pipeline(StandardScaler(),LogisticRegression(solver = 'newton-cg', penalty= 'l2', C= 0.01, max_iter = 5000))

pipeline_lr_tuned.fit(X_train, y_train)

y_pred_lr = pipeline_lr_tuned.predict(X_test)

"""## Results:"""

confusion_matrix(y_test, y_pred_lr)

print(classification_report(y_test, y_pred_lr))

# storing scores in a dictionary
dict_scores[2] = {'Model': 'Logistic Regression', 'State': 'Post-tuning', 'Accuracy': round(accuracy_score(y_test, y_pred_lr),4), 'AUC':round(roc_auc_score(y_test, y_pred_lr),4), 'Blue Win Accuracy':round(recall_score(y_test, y_pred_lr, pos_label=1),4), 'Red Win Accuracy':round(recall_score(y_test, y_pred_lr, pos_label=0),4)}
dict_scores

"""# Logistic Regression with PCA"""

from sklearn.decomposition import PCA

scaler = StandardScaler()

scaled_df = df.copy()

scaled_df=pd.DataFrame(scaler.fit_transform(scaled_df), columns=scaled_df.columns)

pca = PCA(n_components= .80)

pca_fit = pca.fit(scaled_df)

PC_values = np.arange(pca.n_components_) + 1
plt.plot(PC_values, pca.explained_variance_ratio_, 'o-', linewidth=2, color='blue')
plt.title('Scree Plot')
plt.xlabel('Principal Component')
plt.ylabel('Variance Explained')
plt.show()

print(pca.explained_variance_ratio_)

pipeline_lr_tuned_pca = make_pipeline(StandardScaler(), PCA(.80), LogisticRegression(solver = 'newton-cg', penalty= 'l2', C= 0.01, max_iter = 5000))

pipeline_lr_tuned_pca.fit(X_train, y_train)

y_pred_pca = pipeline_lr_tuned_pca.predict(X_test)

"""## Results:"""

confusion_matrix(y_test, y_pred_pca)

print(classification_report(y_test, y_pred_pca))

# storing scores in a dictionary
dict_scores[3] = {'Model': 'Logistic Regression', 'State': 'PCA', 'Accuracy': round(accuracy_score(y_test, y_pred_pca),4), 'AUC':round(roc_auc_score(y_test, y_pred_pca),4), 'Blue Win Accuracy':round(recall_score(y_test, y_pred_pca,pos_label=1),4), 'Red Win Accuracy':round(recall_score(y_test, y_pred_pca,pos_label=0),4)}
dict_scores

"""# LDA"""

# creating an array for shrinkage to tune
shrinkage_parameter= np.linspace(0, 1, 21)
shrinkage_parameter

# setting up hyperparamters to tune
hyperparam_grid = {
    'shrinkage': shrinkage_parameter,
    'solver': ['lsqr', 'eigen'] 
}

# creating model to tune
grid_search_lda= GridSearchCV(estimator= LinearDiscriminantAnalysis(), param_grid=hyperparam_grid, cv=10, scoring='accuracy')

# fitting
grid_search_lda.fit(X_train, y_train)

# best params
grid_search_lda.best_params_

# creating new model
lda_model = LinearDiscriminantAnalysis(shrinkage=0, solver='lsqr')

lda_model.fit(X_train, y_train)

y_pred_lda = lda_model.predict(X_test)

"""## Results:"""

confusion_matrix(y_test, y_pred_lda)

print(classification_report(y_test, y_pred_lda))

# storing scores in a dictionary
dict_scores[4] = {'Model': 'LDA', 'State': 'Post-tuning', 'Accuracy': round(accuracy_score(y_test, y_pred_lda),4), 'AUC':round(roc_auc_score(y_test, y_pred_lda),4), 'Blue Win Accuracy':round(recall_score(y_test, y_pred_lda, pos_label=1),4), 'Red Win Accuracy':round(recall_score(y_test,  y_pred_lda, pos_label=0),4)}
dict_scores

"""## Adjusting Probability Threshold
Checking a hypothesis that the probability threshold is skewed towards blue, and maybe this should be adjusted for
"""

# we'll check probabilities slight above and below .5
array_prob= np.arange(0.495, 0.505, 0.001)

prob_yes= lda_model.predict_proba(X_test)[:,1]

dict_predictions = dict()
dict_accuracy_scores= dict()

for j in array_prob:
    dict_predictions[j]=np.empty(y_test.size, dtype=int)
    for i in np.arange(0, dict_predictions[j].size):
        if prob_yes[i] > j:
            dict_predictions[j][i]= 1
        else:
            dict_predictions[j][i]= 0
    dict_accuracy_scores[j]= np.round (accuracy_score(y_test, dict_predictions[j]),4)

dict_accuracy_scores

max(dict_accuracy_scores, key= dict_accuracy_scores.get)

threshold = max(dict_accuracy_scores, key= dict_accuracy_scores.get)
y_pred_lda_th = (lda_model.predict_proba(X_test)[:,1]>=threshold).astype(int)

"""### Results:"""

confusion_matrix(y_test, y_pred_lda_th)

print(classification_report(y_test, y_pred_lda_th))

"""# Testing the model"""

df.columns

data = [2,1,1,5,5,0,0,0,200,50,0,2,1,0,0,0,200,50]
df_test = pd.DataFrame(data).T
df_test.columns=['blueWardsPlaced', 'blueWardsDestroyed', 'blueFirstBlood',
       'blueKills', 'blueDeaths', 'blueDragons', 'blueHeralds',
       'blueTowersDestroyed', 'blueTotalMinionsKilled',
       'blueTotalJungleMinionsKilled', 'blueGoldDiff', 'redWardsPlaced',
       'redWardsDestroyed', 'redDragons', 'redHeralds', 'redTowersDestroyed',
       'redTotalMinionsKilled', 'redTotalJungleMinionsKilled']

df_test.shape
df_test

df_test['blueKills'][0] = 5
df_test['blueDeaths'][0] = 0

df_test['blueTotalMinionsKilled'][0] = 100
df_test['redTotalMinionsKilled'][0]  = 200

df_test['blueWardsPlaced'][0]=0

df_test['blueTowersDestroyed'][0] = 0

df_test

lda_model.predict_proba(df_test)

"""# Saving the Best Model
(for use in our app)
"""

dict_scores

# saving performance metric scores to .csv file
scores = pd.DataFrame(dict_scores)
scores = scores.T
scores.to_csv('scores.csv')
scores

# .save_model is only an attribute for xgboost models, attempting to save the lda model as a pickle
import pickle
# saving file
pkl_filename = 'lda_save.pkl'
with(open(pkl_filename, 'wb')) as file:
  pickle.dump(lda_model, file)

classifier2.save_model('xgb_model.json')

"""# Making the Game Prediction App"""

# installing and initializing streamlit
!pip install -q streamlit
!pip install pyngrok
!ngrok authtoken streamlit_authorization_code_here
from pyngrok import ngrok 
public_url = ngrok.connect(port='8501')
public_url

df.columns

"""## APP Code"""

# Commented out IPython magic to ensure Python compatibility.
# %%writefile LOL_app.py 
# import xgboost as xgb
# import streamlit as st
# import pandas as pd
# 
# #Loading up the Regression model we created
# model = xgb.XGBRegressor()
# model.load_model('xgb_model.json')
# 
# #Caching the model for faster loading
# @st.cache
# 
# 
# # Define the prediction function
# def predict(wardsDestroyed, blueFirstBlood, blueKills, blueDeaths, blueTowersDestroyed, blueTotalMinionsKilled, blueTotalJungleMinionsKilled, blueGoldDiff, redTowersDestroyed, redTotalMinionsKilled, redTotalJungleMinionsKilled, firstDragon, firstHerald, wardsPlaced):
#     #Predicting the winner
#     if blueFirstBlood == 'Blue':
#         blueFirstBlood = 1
#     elif blueFirstBlood == 'Red':
#         blueFirstBlood = 0
#         blueGoldDiff = blueGoldDiff - 150
# 
#     if firstDragon == 'Blue':
#         blueDragons, redDragons= 1,0
#     elif firstDragon == 'Red':
#         blueDragons, redDragons= 0,1
#     elif firstDragon == 'None':
#         blueDragons, redDragons= 0,0
#     
#     if firstHerald == 'Blue':
#         blueHeralds, redHeralds= 1,0
#     elif firstHerald == 'Red':
#         blueHeralds, redHeralds= 0,1
#     elif firstHerald == 'None':
#         blueHeralds, redHeralds= 0,0
# 
#     if wardsPlaced == 'Blue':
#         blueWardsPlaced, redWardsPlaced= 50,10
#     elif wardsPlaced  == 'Red':
#         blueWardsPlaced, redWardsPlaced= 10,50
#     elif wardsPlaced  == 'Even':
#         blueWardsPlaced, redWardsPlaced= 20,20
# 
#     if wardsDestroyed == 'Blue':
#         blueWardsDestroyed, redWardsDestroyed= 0,10
#     elif wardsDestroyed  == 'Red':
#         blueWardsDestroyed, redWardsDestroyed= 10,0
#     elif wardsDestroyed  == 'Even':
#         blueWardsDestroyed, redWardsDestroyed= 2,2
# 
#     prediction = model.predict(pd.DataFrame([[blueWardsPlaced, blueWardsDestroyed, blueFirstBlood,blueKills, blueDeaths, blueDragons, blueHeralds,blueTowersDestroyed, blueTotalMinionsKilled,blueTotalJungleMinionsKilled, blueGoldDiff, redWardsPlaced,redWardsDestroyed, redDragons, redHeralds, redTowersDestroyed,redTotalMinionsKilled, redTotalJungleMinionsKilled]], columns=['blueWardsPlaced', 'blueWardsDestroyed', 'blueFirstBlood','blueKills', 'blueDeaths', 'blueDragons', 'blueHeralds','blueTowersDestroyed', 'blueTotalMinionsKilled','blueTotalJungleMinionsKilled', 'blueGoldDiff', 'redWardsPlaced','redWardsDestroyed', 'redDragons', 'redHeralds', 'redTowersDestroyed','redTotalMinionsKilled', 'redTotalJungleMinionsKilled']))
#     if prediction>=.5:
#       result = 'Blue Side'
#       return result,prediction
#     else:
#       result = 'Red Side'
#       return result,prediction
# 
# st.markdown("<h2 style='text-align: center; color: black;'>Leauge Of Legends Game Outcome Predictor</h2>", unsafe_allow_html=True)
# st.markdown("<h3 style='text-align: center; color: blue;'>Who Will Win?</h3>", unsafe_allow_html=True)
# 
# 
# 
# st.image("""https://assets-prd.ignimgs.com/2021/12/14/leagueoflegends-1639513774570.jpg""")
# st.markdown("<h1 style='text-align: center;'><u>League of Legends Game Winner Predictor</u></h1>", unsafe_allow_html=True)
# 
# st.header('Enter the game state statistics at 10 minutes:')
# blueGoldDiff = st.number_input('Enter the Gold Difference (Blue team Ahead = positive):', min_value=-10000, max_value=10000, value=0)
# blueKills = st.number_input('How many kills does Blue side have?', min_value=0, max_value=50, value=10)
# blueDeaths = st.number_input('How many kills does Red side have?', min_value=0, max_value=50, value=10)
# blueFirstBlood = st.selectbox('Who had first blood?', ['Blue', 'Red'])
# firstDragon = st.selectbox('Who killed first dragon?', ['None','Blue', 'Red'])
# firstHerald = st.selectbox('Who killed first herald?', ['None','Blue', 'Red'])
# redTowersDestroyed =st.number_input('How many towers did Blue destroy?', min_value=0, max_value=5, value=1)
# blueTowersDestroyed =st.number_input('How many towers did Red destroy?', min_value=0, max_value=5, value=1)
# blueTotalMinionsKilled =st.number_input('How many total minions did Blue side kill?', min_value=130, max_value=280, value=216)
# redTotalMinionsKilled =st.number_input('How many total minions did Red side kill?', min_value=130, max_value=280, value=216)
# blueTotalJungleMinionsKilled =st.number_input('How many total Jungle minions did Blue side kill?', min_value=20, max_value=90, value=50)
# redTotalJungleMinionsKilled =st.number_input('How many total Jungle minions did Red side kill?', min_value=20, max_value=90, value=50)
# wardsPlaced = st.selectbox('Who placed more wards?', ['Even','Blue', 'Red'])
# wardsDestroyed = st.selectbox('Who destroyed more wards?', ['Even','Blue', 'Red'])
# 
# 
# 
# 
# if st.button('Predict the Winner'):
#     winner,prediction = predict(wardsDestroyed, blueFirstBlood, blueKills, blueDeaths, blueTowersDestroyed, blueTotalMinionsKilled, blueTotalJungleMinionsKilled, blueGoldDiff, redTowersDestroyed, redTotalMinionsKilled, redTotalJungleMinionsKilled, firstDragon, firstHerald, wardsPlaced)
#     st.success(f'The predicted winner is {winner}, {prediction}')
# 
# st.sidebar.image('https://www.leagueoflegends.com/static/open-graph-2e582ae9fae8b0b396ca46ff21fd47a8.jpg', width=250)
# with st.sidebar:
#     st.subheader('About')
#     st.markdown('This dashboard is brought to you by Frank and Michael, using **Streamlit**')
# 
# 
# # caching dataset
# #@st.cache
# #def load_data(path):
# #    dataset = pd.read_csv(path)
# #    return dataset
# #car = load_data('https://raw.githubusercontent.com/fenago/datasets/main/car%20data.csv')

"""## Running the app"""

!streamlit run /content/LOL_app.py & npx localtunnel --port 8501

np.mean(df['blueTotalJungleMinionsKilled'])
min(df['blueTotalJungleMinionsKilled'])

max(df['redWardsDestroyed'])

"""# References
- https://towardsdatascience.com/bayesian-optimization-with-python-85c66df711ec
- https://coderzcolumn.com/tutorials/machine-learning/bayes-opt-bayesian-optimization-for-hyperparameters-tuning
- https://venturebeat.com/games/league-of-legends-worlds-2022-sets-peak-viewership-record/
- https://www.kaggle.com/datasets/bobbyscience/league-of-legends-diamond-ranked-games-10-min
"""
