import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

import joblib

df = pd.read_csv("ml/leads.csv")

X = df.drop("converted", axis=1)

y = df["converted"]

categorical = [
    "industry",
    "title"
]

numeric = [
    "company_size",
    "pricing_views",
    "email_opens"
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categorical
        )
    ],
    remainder="passthrough"
)

model = Pipeline([
    ("prep", preprocessor),
    ("clf", LogisticRegression(max_iter=1000))
])

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model.fit(X_train, y_train)

preds = model.predict(X_test)

acc = accuracy_score(
    y_test,
    preds
)

print(f"Accuracy: {acc:.3f}")

joblib.dump(
    model,
    "ml/lead_model.pkl"
)

print("Model saved")