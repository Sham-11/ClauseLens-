import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Step 1: Load CUAD data
with open("data/CUADv1.json", "r") as f:
    raw_data = json.load(f)

data = raw_data["data"]

texts = []
labels = []

# Step 2: Extract training samples (context, clause_type)
for entry in data:
    for para in entry["paragraphs"]:
        context = para["context"]
        for qa in para["qas"]:
            if not qa["is_impossible"]:
                clause_type = qa["question"].split('"')[1] if '"' in qa["question"] else qa["question"]
                texts.append(context)
                labels.append(clause_type)

# Step 3: Split and train
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=10000, stop_words="english")),
    ("clf", LogisticRegression(max_iter=1000))
])

pipeline.fit(X_train, y_train)

# Step 4: Evaluate
y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred))

# Step 5: Save model
os.makedirs("models", exist_ok=True)
joblib.dump(pipeline, "models/cuad_clause_classifier.pkl")
print("Model saved to models/cuad_clause_classifier.pkl")
