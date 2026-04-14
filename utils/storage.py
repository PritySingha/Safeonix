import pandas as pd
import os
from datetime import datetime

DATA_PATH = "data/transactions.csv"

COLUMNS = [
    "timestamp", "type", "amount",
    "oldbalanceOrg", "newbalanceOrig",
    "oldbalanceDest", "newbalanceDest",
    "probability", "label", "is_fraud"
]


def load_transactions() -> pd.DataFrame:
    if not os.path.exists(DATA_PATH):
        return pd.DataFrame(columns=COLUMNS)
    
    df = pd.read_csv(DATA_PATH, parse_dates=["timestamp"])
    
    # Convert is_fraud from string/boolean to int (0/1) for consistency
    if "is_fraud" in df.columns:
        # If it's object (string) or bool, map to int
        if df["is_fraud"].dtype == "object" or df["is_fraud"].dtype == "bool":
            df["is_fraud"] = df["is_fraud"].astype(str).map({"True": 1, "False": 0}).fillna(0).astype(int)
        else:
            df["is_fraud"] = df["is_fraud"].astype(int)
    
    return df


def save_transaction(record: dict):
    # Ensure is_fraud is stored as int (0/1) to avoid "True"/"False" strings
    if "is_fraud" in record:
        record["is_fraud"] = int(record["is_fraud"])
    
    record["timestamp"] = datetime.now().isoformat()
    df_new = pd.DataFrame([record])

    if os.path.exists(DATA_PATH):
        df_new.to_csv(DATA_PATH, mode="a", header=False, index=False)
    else:
        os.makedirs("data", exist_ok=True)
        df_new.to_csv(DATA_PATH, mode="w", header=True, index=False)