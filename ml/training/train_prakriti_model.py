"""
train_prakriti_model.py
-----------------------

Trains a machine learning model to predict Prakriti
(Vata / Pitta / Kapha) from questionnaire inputs.
"""

import os
import sys
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.utils import resample


# -----------------------------
# Path setup
# -----------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ML_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.append(ML_DIR)

DATA_PATH = os.path.join(ML_DIR, "data", "Prakriti.csv")
MODEL_DIR = os.path.join(ML_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "prakriti_model.pkl")
ENCODER_PATH = os.path.join(MODEL_DIR, "prakriti_label_encoder.pkl")


# -----------------------------
# Convert Dual Dosha → Single Dosha
# -----------------------------
def convert_to_single_dosha(label: str) -> str:
    label = label.lower().strip()

    if "vata" in label:
        return "Vata"
    elif "pitta" in label:
        return "Pitta"
    elif "kapha" in label:
        return "Kapha"
    else:
        return label.capitalize()


# -----------------------------
# Balance Dataset
# -----------------------------
def balance_dataset(df):
    print("\n📊 Original Class Distribution:")
    print(df["prakriti"].value_counts())

    min_count = df["prakriti"].value_counts().min()

    balanced_df = pd.DataFrame()

    for cls in df["prakriti"].unique():
        class_df = df[df["prakriti"] == cls]
        class_sample = resample(
            class_df,
            replace=False,
            n_samples=min_count,
            random_state=42
        )
        balanced_df = pd.concat([balanced_df, class_sample])

    print("\n📊 Balanced Class Distribution:")
    print(balanced_df["prakriti"].value_counts())

    return balanced_df.sample(frac=1, random_state=42).reset_index(drop=True)


# -----------------------------
# Main Training Function
# -----------------------------
def main():
    print("🔹 Loading Prakriti dataset...")
    df = pd.read_csv(DATA_PATH)

    # Normalize column names
    df.columns = df.columns.str.lower().str.strip()

    if "dosha" not in df.columns:
        raise ValueError("❌ 'dosha' column not found in dataset.")

    df = df.rename(columns={"dosha": "prakriti"})

    # Convert to single dosha
    df["prakriti"] = df["prakriti"].apply(convert_to_single_dosha)

    print("\n📊 New Class Distribution:")
    print(df["prakriti"].value_counts())

    # Balance dataset
    df = balance_dataset(df)

    # -----------------------------
    # Features & Label
    # -----------------------------
    X = df.drop(columns=["prakriti"])
    y = df["prakriti"].astype(str)

    # Encode label
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # Categorical encoding
    categorical_cols = X.columns.tolist()

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
        ]
    )

    # -----------------------------
    # Train-test split (STRATIFIED)
    # -----------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y_encoded,
        test_size=0.25,
        random_state=42,
        stratify=y_encoded
    )

    # -----------------------------
    # Controlled RandomForest
    # -----------------------------
    model = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(
            n_estimators=120,
            max_depth=8,
            min_samples_leaf=3,
            random_state=42
        ))
    ])

    print("\n🔹 Training Prakriti classification model...")
    model.fit(X_train, y_train)

    # -----------------------------
    # Evaluation
    # -----------------------------
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    print("\n✅ Training Completed")
    print(f"📊 Accuracy: {accuracy * 100:.2f}%\n")

    print("📄 Classification Report:")
    print(classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_
    ))

    # -----------------------------
    # Save model
    # -----------------------------
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(label_encoder, ENCODER_PATH)

    print(f"\n💾 Model saved at: {MODEL_PATH}")
    print(f"💾 Label encoder saved at: {ENCODER_PATH}")


if __name__ == "__main__":
    main()
