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
import joblib

# Importing the data, Full data description --> https://www.kaggle.com/amanajmera1/framingham-heart-study-dataset
BASE_DIR = os.path.dirname(__file__)
DATASET_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

class HeartDiseaseModel:

    def __init__(self):
        self.features = ['sysBP','glucose','age','totChol','cigsPerDay','diaBP','prevalentHyp','diabetes','BPMeds','male','BMI','prevalentStroke']
        self.model_path = os.path.join(MODELS_DIR, 'heart-prediction-model.pkl')

    def save_model(self):
        """ Model Serialization """
        self.model = self.train_model()
        joblib.dump(self.model, self.model_path)
    
    def load_model(self):
        """ Model De-serialization """
        self.model = joblib.load(self.model_path)
    
    def train_model(self):
        self.df = pd.read_csv(os.path.join(DATASET_DIR, 'framingham.csv')).dropna()
        model = RandomForestClassifier(max_depth=8, max_features='sqrt', n_estimators=900)
        X = self.df[self.features]
        target = self.df.iloc[:, -1]
        model.fit(X, target)
        return model

    def predict(self, data : dict):
        print(data)
        male_enc = {"female" : 0, "male" : 1}
        bpmeds_enc = {"yes" : 1, "no" : 0}
        diabetes_enc = {"yes" : 1, "no" : 0}
        prevalence_enc = {"yes" : 1, "no" : 0}
        bmi = data["weight"] / data["height"]
        features = [data["sysBP"], data["glucose"], data["age"], data["totChol"], data["cigsPerDay"], data["diaBP"], prevalence_enc[data["prevalentHyp"].lower()], diabetes_enc[data["diabetes"].lower()], bpmeds_enc[data["BPMeds"].lower()], male_enc[data["gender"].lower()], bmi, prevalence_enc[data["prevalentStroke"].lower()]]
        data = np.array([features])
        prediction = self.model.predict(data)
        prediction_prob = self.model.predict_proba(data).max()
        response = {
            "prediction" : int(prediction[0]),
            "probability" : np.round(prediction_prob, 2)
        }
        print(response)
        return response


if __name__ == "__main__":
    heartdisease = HeartDiseaseModel()
    # heartdisease.save_model()
    heartdisease.load_model()
    data = {
        "sysBP" : 40, "glucose" : 20, "age" : 12, "totChol" : 130,
        "cigsPerDay" : 1, "diaBP" : 10, "prevalentHyp" : "Yes", "diabetes" : "Yes", "BPMeds" : "No",
        "gender" : "Male", "weight" : 23, "height" : 4, "prevalentStroke" : "Yes"
    }
    print(heartdisease.predict(data))



