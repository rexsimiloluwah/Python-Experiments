import os
from pathlib import Path
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.model_selection import train_test_split, cross_val_score, RandomizedSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.metrics import f1_score, classification_report, accuracy_score, confusion_matrix
from sklearn.linear_model import LogisticRegression 
from sklearn.ensemble import RandomForestClassifier 
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.svm import SVC
import seaborn as sns

# Importing the data, Full data description --> https://www.kaggle.com/amanajmera1/framingham-heart-study-dataset
DATASET_DIR = "./data"
data = pd.read_csv(os.path.join(DATASET_DIR, 'framingham.csv'))
# print(data.shape) --> (4240, 16)
# print(data.columns)
# print(data.head())
print(data.info())

# Check for null values 
print(data.isnull().sum().sort_values(ascending = False))

# Dropping all null values (not advisable)
data = data.dropna()

# print(data.shape)

# Check correlation between features
corr_matrix = data.corr()
print(corr_matrix)
highly_corr_matrix = np.where(abs(corr_matrix) > 0.5)
print(highly_corr_matrix)

print([[corr_matrix.index[x], corr_matrix.index[y], corr_matrix.values[x,y]] for (x,y) in dict(zip(highly_corr_matrix[0].tolist(), highly_corr_matrix[1].tolist())).items() if x != y])

# Selecting Best features 
X = data.iloc[:, 0:15]
y = data.iloc[:, -1]

# Apply KBest to extract 10 best features 
best = SelectKBest(score_func = chi2, k = 10)
fit = best.fit(X, y)

# print(pd.concat([pd.DataFrame(X.columns), pd.DataFrame(fit.scores_)], axis = 1))
scores = pd.concat([pd.DataFrame(X.columns), pd.DataFrame(fit.scores_)], axis = 1)
scores.columns = ["Feature", "Score"]
print(scores.nlargest(12, "Score")["Feature"].values)

# Features that have the strongest influence on the target variable --> ['sysBP','glucose','age','totChol','cigsPerDay','diaBP','prevalentHyp','diabetes','BPMeds','male','BMI','prevalentStroke']

features = scores.nlargest(12, "Score")["Feature"].values
X = data[features] 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, stratify = y, random_state = 42)
print(X_train.shape, X_test.shape)

model = KNeighborsClassifier()
model.fit(X_train, y_train)

print(classification_report(model.predict(X_test), y_test))

def plot_confusion_matrix(model):
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_pred, y_test)
    fig, ax = plt.subplots(figsize = (12, 12))
    sns.heatmap(cm,annot = True,cmap='Reds',linewidths=1,linecolor='k',square=True,mask=False,fmt = ".0f",cbar=True, ax = ax)
    plt.xlabel("Y_predicted")
    plt.ylabel("Y_true")
    plt.show()

models = []
models.append(('LogisticRegression', LogisticRegression()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('RandomForest', RandomForestClassifier()))
models.append(('SVM', SVC()))

for (name, model) in models:
    model.fit(X_train, y_train)
    f1_score = cross_val_score(model, X_train, y_train, cv=10, scoring = "f1_weighted").mean()
    roc_auc_score = cross_val_score(model, X_train, y_train, cv=10, scoring = "roc_auc").mean()
    print(f"{name}, F1 Score = {f1_score}, ROC AUC Score = {roc_auc_score}")
    plot_confusion_matrix(model)
    

# Hyperparameter tuning for the best performing model - RandomForestClassifier

# Creating the parameter distribution
# N-estimators (Number of trees in the random forest)
n_estimators = np.linspace(100, 1000, num = 10).astype(int)
# Max-depth 
max_depth = np.arange(2, 10, 2).astype(int)
# Min-samples-leaf
min_samples_leaf = np.arange(1,5).astype(int)
# Min-samples-split
min_samples_split = [2, 3, 5, 7]
# Max-features (features considered on every split)
max_features = ["auto", "sqrt"]

random_grid = {
    "n_estimators" : n_estimators,
    "max_depth" : max_depth,
    "min_samples_leaf" : min_samples_leaf,
    "min_samples_split"  : min_samples_split,
    "max_features" : max_features
}

print(random_grid)

model = RandomForestClassifier()

tuned_model = RandomizedSearchCV(
    estimator = model,
    param_distributions= random_grid,
    n_iter = 50,
    verbose = 4,
    cv = 3,
    random_state = 2001,
    n_jobs = -1,
    scoring = "f1"
)

# tuned_model.fit(X_train, y_train)

# print(tuned_model.best_estimator_)

rf_tuned = RandomForestClassifier(max_depth=8, max_features='sqrt', n_estimators=900)

rf_tuned.fit(X_train, y_train)

plot_confusion_matrix(rf_tuned)