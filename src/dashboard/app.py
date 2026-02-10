import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import time

st.set_page_config(page_title="LLM Eval Dashboard", layout="wide")
st.title("📊 LLM Evaluation & Governance Dashboard")

# Connect to DB
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/evaldb")
engine = create_engine(DATABASE_URL)

@st.cache_data(ttl=5)
def load_data():
    try:
        return pd.read_sql("SELECT * FROM evaluation_runs ORDER BY created_at DESC", engine)
    except Exception:
        return pd.DataFrame() # Return empty if DB not ready

data = load_data()

if not data.empty:
    st.subheader("Recent Runs")
    st.dataframe(data)

    st.subheader("Performance Trends")
    col1, col2 = st.columns(2)
    with col1:
        st.line_chart(data.set_index("created_at")["avg_accuracy"])
        st.caption("Accuracy Over Time")
    with col2:
        st.line_chart(data.set_index("created_at")["avg_latency"])
        st.caption("Latency (ms)")
else:
    st.info("No evaluation runs found yet. Trigger one via the API!")

if st.button("Refresh Data"):
    st.rerun()
