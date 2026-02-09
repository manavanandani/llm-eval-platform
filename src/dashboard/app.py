import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="LLM Eval Dashboard", layout="wide")

st.title("📊 LLM Evaluation & Governance Dashboard")

st.sidebar.header("Filter Runs")
selected_model = st.sidebar.selectbox("Select Model", ["gpt-4-turbo", "gemini-pro", "llama-3-70b"])

# Mock Data
data = pd.DataFrame({
    "run_id": ["run_101", "run_102", "run_103"],
    "timestamp": ["2024-02-01", "2024-02-02", "2024-02-03"],
    "accuracy": [0.82, 0.84, 0.88],
    "hallucination_rate": [0.12, 0.10, 0.05],
    "avg_latency_ms": [450, 430, 410]
})

st.subheader("Performance Trends")
col1, col2 = st.columns(2)
with col1:
    st.line_chart(data.set_index("timestamp")["accuracy"])
    st.caption("Accuracy Over Time")
with col2:
    st.line_chart(data.set_index("timestamp")["hallucination_rate"])
    st.caption("Hallucination Rate (Lower is Better)")

st.subheader("Recent Runs")
st.dataframe(data)
