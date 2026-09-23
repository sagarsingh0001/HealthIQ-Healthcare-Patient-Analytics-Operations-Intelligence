import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                              f1_score, classification_report, confusion_matrix)
import joblib
import os

df = pd.read_csv('data/processed/cleaned_healthcare_data.csv',
                 parse_dates=['visit_date'])

features = ['age_group', 'gender', 'region', 'department', 'treatment_type', 'visit_type',
            'length_of_stay_days', 'treatment_cost', 'recovery_score']
target = 'readmission_risk'

X = df[features]
y = df[target]

cat_features = ['age_group', 'gender', 'region', 'department', 'treatment_type', 'visit_type']
num_features = ['length_of_stay_days', 'treatment_cost', 'recovery_score']

preprocessor = ColumnTransformer(transformers=[
    ('cat', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1), cat_features),
    ('num', StandardScaler(), num_features)
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

models = {
    'Logistic Regression': LogisticRegression(
        max_iter=500, random_state=42, class_weight='balanced'),
    'Decision Tree': DecisionTreeClassifier(
        max_depth=6, random_state=42, class_weight='balanced'),
    'Random Forest': RandomForestClassifier(
        n_estimators=100, max_depth=8, random_state=42, n_jobs=-1, class_weight='balanced'),
}

results = {}
for name, model in models.items():
    pipe = Pipeline([('preprocessor', preprocessor), ('model', model)])
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(pipe, X_train, y_train, cv=cv, scoring='f1_weighted')
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    f1  = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    rec  = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    results[name] = {
        'pipeline': pipe, 'cv_f1': cv_scores.mean(), 'cv_std': cv_scores.std(),
        'test_acc': acc, 'f1': f1, 'prec': prec, 'rec': rec, 'y_pred': y_pred
    }
    print(f"{name}: CV_F1={cv_scores.mean():.3f}(+/-{cv_scores.std():.3f})  "
          f"TestAcc={acc:.3f}  F1={f1:.3f}  Prec={prec:.3f}  Rec={rec:.3f}")

best_name = max(results, key=lambda x: results[x]['f1'])
best = results[best_name]
pipe = best['pipeline']
y_pred = best['y_pred']

print(f"\nBest model: {best_name}")
print()
print(classification_report(y_test, y_pred, zero_division=0))
print("Confusion matrix (Low / Medium / High):")
print(confusion_matrix(y_test, y_pred, labels=['Low', 'Medium', 'High']))

joblib.dump(pipe, 'models/readmission_risk_pipeline.pkl')
print(f"\nSaved pipeline for: {best_name}")
print("CV F1  :", round(best['cv_f1'], 3))
print("Test Acc:", round(best['test_acc'], 3))
print("F1     :", round(best['f1'], 3))
