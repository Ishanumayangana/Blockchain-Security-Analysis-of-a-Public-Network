import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import seaborn as sns
import matplotlib.pyplot as plt
from src.data_loader import generate_synthetic_contract_data

def train_vulnerability_classifier(df):
    """
    Trains a Random Forest classifier to detect vulnerable contracts.
    """
    X = df.drop('vulnerable', axis=1)
    y = df['vulnerable']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    y_pred = clf.predict(X_test)
    
    print("Model Evaluation:")
    print(classification_report(y_test, y_pred))
    
    return clf, X_test, y_test, y_pred

def plot_feature_importance(clf, feature_names):
    """
    Plots the importance of each feature in the trained model.
    """
    importances = clf.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=importances[indices], y=np.array(feature_names)[indices], palette="magma")
    plt.title("Feature Importance for Vulnerability Detection")
    plt.show()
