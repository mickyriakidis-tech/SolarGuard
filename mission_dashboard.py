import streamlit as st
import pandas as pd
from dashboard_data import load_audit_data

st.set_page_config(
    page_title="SolarGuard 2.0",
    page_icon="🛰️",
    layout="wide"
)

st.title("🛰️ SolarGuard 2.0")
st.subheader("Mission Control Dashboard")
st.caption("Audit Trail Monitoring")

if st.button("Refresh Mission Data"):
    st.rerun()

try:
    df = load_audit_data()
except FileNotFoundError as error:
    st.error(str(error))
    st.stop()
except ValueError as error:
    st.error(str(error))
    st.stop()
except Exception as error:
    st.error(f"Could not read audit data: {error}")
    st.stop()

st.header("Audit Data Quality")

total_records = len(df)
invalid_records = df[["risk_score", "energy", "timestamp"]].isna().any(axis=1).sum()
valid_records = total_records - invalid_records

q_col1, q_col2, q_col3 = st.columns(3)
q_col1.metric("Total Records", total_records)
q_col2.metric("Valid Records", valid_records)
q_col3.metric("Records Needing Review", invalid_records)

clean_df = df.dropna(subset=["risk_score", "energy", "timestamp"])

if clean_df.empty:
    st.warning("No valid records available.")
    st.stop()

latest = clean_df.iloc[-1]

risk = float(latest["risk_score"])
energy = float(latest["energy"]) * 100
decision = str(latest["action"])
reason = str(latest.get("reason", "N/A"))

st.header("Mission Status")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Risk Index", f"{risk:.2f}")

with col2:
    st.metric("Energy", f"{energy:.1f}%")

with col3:
    st.metric("Last Decision", decision)

st.header("Recommended Action")

if decision == "NORMAL":
    st.success(f"NORMAL - {reason}")
elif decision == "PROTECTIVE":
    st.warning(f"PROTECTIVE - {reason}")
elif decision == "LIMITED":
    st.info(f"LIMITED - {reason}")
else:
    st.error(f"Unknown decision status: {decision}")

st.header("Risk History")
st.line_chart(clean_df.set_index("timestamp")["risk_score"])

st.header("Energy History")
st.line_chart(clean_df.set_index("timestamp")["energy"])

st.header("Decision Audit Trail")
st.dataframe(
    df.sort_values("timestamp", ascending=False),
    width="stretch"
)

st.header("Mission Summary")
st.write(f"Total recorded decisions: {total_records}")
st.write(f"Valid numeric records: {valid_records}")
st.write("This dashboard displays live audit trail records.")
