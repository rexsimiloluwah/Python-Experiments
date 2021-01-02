import os, json, pickle
from pathlib import Path 
import numpy as np
import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt 
from sklearn.model_selection import cross_val_score, train_test_split 
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from .helpers import remove_stopwords, remove_unwanted_chars, clean_apostrophe_slangs, normalize

# Importing the data, Full data description --> https://www.kaggle.com/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews
BASE_DIR = os.path.dirname(__file__)
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# TF-IDF
tvect = TfidfVectorizer(min_df=3,  max_features=None, 
            strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',
            ngram_range=(1, 3), use_idf=1,smooth_idf=1,sublinear_tf=1,
            stop_words = 'english')

def plot_confusion_matrix(model, X_test, y_test):
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_pred, y_test)
    fig, ax = plt.subplots(figsize = (12, 12))
    sns.heatmap(cm,annot = True,cmap='Reds',linewidths=1,linecolor='k',square=True,mask=False,fmt = ".0f",cbar=True, ax = ax)
    plt.xlabel("Y_predicted")
    plt.ylabel("Y_true")
    plt.show()

class MoviesSentimentModel:

    def __init__(self):
        self.model_path = os.path.join(MODELS_DIR, 'moviessentimentmodel.pkl')
        self.vectorizer_path = os.path.join(MODELS_DIR, 'vectorizer.pkl')
    
    def analyse_data(self):
        return self.df.head()

    def _train(self):
        self.df = pd.read_csv(os.path.join(DATASET_DIR, 'preprocessed_train_data.csv'))
        self.X = self.df["cleaned_text"]
        mapper = {"positive":1, "negative" : 0}
        self.target = self.df["sentiment"].map(mapper)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.target, test_size = 0.1, random_state = 2001)
        tvect.fit(self.X_train.values.tolist())
        self.X_train_tvect = tvect.transform(self.X_train.values)
        self.X_test_tvect = tvect.transform(self.X_test.values)
        model = LogisticRegression()
        model.fit(self.X_train_tvect, self.y_train)
        pickle.dump(tvect, open(self.vectorizer_path, "wb"))
        return model 

    def _save_model(self):
        model = self._train()
        pickle.dump(model, open(self.model_path, "wb"))

    def _load_model(self):
        self.model = pickle.load(open(self.model_path, "rb"))
        self.vectorizer = pickle.load(open(self.vectorizer_path, "rb"))

    def predict(self, text):
        self._load_model()
        cleaned_text = remove_stopwords(text)
        cleaned_text = remove_unwanted_chars(cleaned_text)
        cleaned_text = normalize(cleaned_text)
        arr = self.vectorizer.transform([cleaned_text]).toarray()
        return {
            "prediction" : int(self.model.predict(arr)[0]),
            "probability" : self.model.predict_proba(arr).max()
        }

    
    def test(self):
        model = self._train()
        plot_confusion_matrix(model, self.X_test_tvect, self.y_test)


import time
if __name__ == "__main__":
    start = time.time()
    msm = MoviesSentimentModel()
    # print(msm.analyse_data())
    msm._save_model()
    print(msm.predict("The movie is not interesting."))
    end = time.time()
    print(end - start)
