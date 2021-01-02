import os, re, json
import numpy as np 
import nltk
from nltk.corpus import words, stopwords
from nltk.stem import PorterStemmer

# nltk.download('words')
BASE_DIR = os.path.dirname(__file__)
apostrophe_slangs = json.load(open(os.path.join(BASE_DIR, 'apostrophe_slangs.json')))
stopwords = stopwords.words('english')
english_words = words.words()
porterstemmer = PorterStemmer()

def clean_apostrophe_slangs(sentence):
    tokens = []
    for word in sentence.split(" "):
        if word in apostrophe_slangs.keys():
            cleaned_word = apostrophe_slangs[word]
        else:
            cleaned_word = word 
        tokens.append(cleaned_word)
    return " ".join(tokens)

def remove_stopwords(sentence):
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
    for word in sentence.split(" "):
        tokens.append(re.sub(combined_pattern_removal, "", word).strip())
    return " ".join([token for token in tokens if token != ""])

def normalize(sentence):
    tokens = []
    for word in sentence.split(" "):
        stemmed = porterstemmer.stem(word)
        if stemmed in english_words:
            tokens.append(stemmed)
        else:
            tokens.append(word)
    return " ".join(list(set(tokens)))