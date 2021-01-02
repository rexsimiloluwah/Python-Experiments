import os, re, json
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
import nltk
from nltk.corpus import words, stopwords
from nltk.stem import PorterStemmer

# nltk.download('words')

# Importing the data, Full data description --> https://www.kaggle.com/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews
DATASET_DIR = "./dataset"
data = pd.read_csv(os.path.join(DATASET_DIR, 'IMDB Dataset.csv'))

# print(data.head())
# print(f"Dataset shape :- {data.shape}")
# print(data.isnull().sum())
# print(data["sentiment"].value_counts())

apostrophe_slangs = json.load(open("./apostrophe_slangs.json"))
stopwords = stopwords.words('english')
english_words = words.words()
porterstemmer = PorterStemmer()

# Cleaning 
data["cleaned_text"] = data["review"].apply(lambda x : x.lower())
print(data.sample())

# Train with 10000 samples 
X_train, X_test, y_train, y_test = train_test_split(data[["cleaned_text", "review"]], data["sentiment"], stratify = data["sentiment"], train_size = 0.2, random_state = 2001)

train_data = pd.concat([X_train, y_train], axis = 1)

def clean_apostrophe_slangs(sentence):
    print("[PROCESS] :- Started Cleaning Apostrophe slangs")
    tokens = []
    for word in sentence.split(" "):
        if word in apostrophe_slangs.keys():
            cleaned_word = apostrophe_slangs[word]
        else:
            cleaned_word = word 
        tokens.append(cleaned_word)
    print(tokens)
    return " ".join(tokens)

def remove_stopwords(sentence):
    print("[PROCESS] :- Started removing stop words")
    tokens = []
    for word in sentence.split(" "):
        if word not in list(set(stopwords) - {'no', 'nor', 'not', 'now', 'being', 'having', 'against'}):
            tokens.append(word)
        else: 
            pass 
    print(tokens)
    return " ".join(tokens)

def remove_unwanted_chars(sentence):
    tokens = []
    mentions_pattern = r'@[A-Za-z0-9_]+'
    hashtag_pattern = r'#[A-Za-z0-9_]+'
    http_pattern = r'http(s?)://[^ ]+'
    www_pattern = r'www.[^ ]+'
    punct_pattern = r'[!"\$%&\'()*+,\-.\/:;=#@?\[\\\]^_`{|}~]*'
    numbers_pattern = r'[0-9]+'
    newline_pattern = r'\n'
    non_alphabets = r'[^a-zA-Z]+'
    combined_pattern_removal = r'|'.join((numbers_pattern, http_pattern, mentions_pattern, punct_pattern, www_pattern, hashtag_pattern, newline_pattern, non_alphabets))
    print("[PROCESS] :- Started removing unwanted characters")
    for word in sentence.split(" "):
        tokens.append(re.sub(combined_pattern_removal, "", word).strip())
    print(tokens)
    return " ".join([token for token in tokens if token != ""])

def normalize(sentence):
    print("[PROCESS] :- Started normalizing and stemming text to reduce inflection.")
    tokens = []
    for word in sentence.split(" "):
        stemmed = porterstemmer.stem(word)
        if stemmed in english_words:
            tokens.append(stemmed)
        else:
            tokens.append(word)
    print(tokens)
    return " ".join(list(set(tokens)))

# print(normalize("I want to sing and singing and making previous commenters and climax and delivery it sound like he sings br br br"))
# print(remove_stopwords("i want to not be against this is the would not make it"))

# train_data["cleaned_text"] = train_data["cleaned_text"].apply(lambda x: clean_apostrophe_slangs(x))
# print("[PROCESS] : Finished cleaning apostrophe slangs.")
# train_data["cleaned_text"] = train_data["cleaned_text"].apply(lambda x : remove_stopwords(x))
# print("[PROCESS] : Finished removing stop words.")
# train_data["cleaned_text"] = train_data["cleaned_text"].apply(lambda x: remove_unwanted_chars(x))
# print("[PROCESS] : Finshed removing unwanted characters")
# train_data["cleaned_text"] = train_data["cleaned_text"].apply(lambda x : normalize(x))
# print("[PROCESS] : Finished normalizing to reduce inflection")

# train_data.to_csv(os.path.join(DATASET_DIR, "preprocessed_train_data.csv"), index = False)

