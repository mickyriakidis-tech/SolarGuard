import pandas as pd
import streamlit as st
from pathlib import Path

AUDIT_FILE = Path("solarguard_audit.csv")

@st.cache_data(ttl=2)
def load_audit_data() -> pd.DataFrame:
    if not AUDIT_FILE.exists():
        raise FileNotFoundError(f"File not found: {AUDIT_FILE}")

    df = pd.read_csv(AUDIT_FILE)

    if df.empty:
        raise ValueError("Audit trail file is empty.")

    required_columns = ["timestamp", "risk_score", "action", "energy"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    for col in ["risk_score", "energy"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df
