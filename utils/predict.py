import pickle
import numpy as np
import pandas as pd

# Load model once
with open("models/fraud_model.pkl", "rb") as f:
    MODEL = pickle.load(f)

with open("models/columns.pkl", "rb") as f:
    COLUMNS = pickle.load(f)


def predict_fraud(input_data: dict) -> dict:
    """
    Predict fraud probability

    Required keys:
    type
    amount
    oldbalanceOrg
    newbalanceOrig
    oldbalanceDest
    newbalanceDest
    """

    # Convert to dataframe
    df = pd.DataFrame([input_data])

    # --------------------------
    # Feature Engineering
    # --------------------------
    df["sender_diff"] = df["oldbalanceOrg"] - df["newbalanceOrig"]

    df["receiver_diff"] = (
        df["newbalanceDest"] - df["oldbalanceDest"]
    )

    df["amount_ratio"] = df["amount"] / (df["oldbalanceOrg"] + 1)

    # --------------------------
    # One Hot Encoding
    # --------------------------
    df = pd.get_dummies(df, columns=["type"])

    # --------------------------
    # Align Columns
    # --------------------------
    for col in COLUMNS:
        if col not in df.columns:
            df[col] = 0

    df = df[COLUMNS]

    # --------------------------
    # Prediction
    # --------------------------
    prob = float(MODEL.predict_proba(df)[0][1])

    is_fraud = prob >= 0.5

    # Risk Labels
    if prob < 0.40:
        label = "SAFE"
    elif prob < 0.70:
        label = "MEDIUM RISK"
    else:
        label = "HIGH RISK"

    return {
        "probability": round(prob, 4),
        "label": label,
        "is_fraud": is_fraud
    }