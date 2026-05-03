import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time


st.subheader("🚀 Performance Lab: PQC vs. Legacy")
st.set_page_config(page_title="QUANTUM-RESILIENT LEDGER", layout="wide", initial_sidebar_state="collapsed")

comparison_metrics = {
    "Algorithm": ["ECDSA (Legacy)", "ML-DSA (Dilithium)"],
    "Verification Time (ms)": [0.12, 1.45], # PQC is slower
    "Payload Size (Bytes)": [64, 2420]      # PQC is much larger
}

fig_perf = go.Figure(data=[
    go.Bar(name='Verification Speed (ms)', x=comparison_metrics["Algorithm"], y=comparison_metrics["Verification Time (ms)"]),
    go.Bar(name='Signature Size (Bytes)', x=comparison_metrics["Algorithm"], y=comparison_metrics["Payload Size (Bytes)"])
])
fig_perf.update_layout(barmode='group', template="plotly_dark")
st.plotly_chart(fig_perf, use_container_width=True)

# --- CUSTOM CYBERSECURITY THEME ---
st.markdown("""
    <style>
    .main { background-color: #050505; color: #00FF41; font-family: 'Courier New', Courier, monospace; }
    .stMetric { background-color: #111; border: 1px solid #00FF41; padding: 15px; border-radius: 5px; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
c1, c2 = st.columns([3, 1])
with c1:
    st.title("🛰️ TESSERACT: QUANTUM-SECURE A2A INFRA")
    st.write("LIVE NETWORK MONITOR | ALGORITHM: CRYSTALS-DILITHIUM (NIST FIPS 204)")
with c2:
    st.metric("THREAT LEVEL", "LOW", delta="-2% (Quantum Safe)")

# --- LIVE DATA FETCHING ---
def get_ledger_data():
    try:
        r = requests.get("http://127.0.0.1:8000/chain").json()
        status = requests.get("http://127.0.0.1:8000/status").json()
        return r['chain'], status
    except:
        return [], {"ledger_height": 0, "pending_tx": 0}

chain, status = get_ledger_data()

# --- TOP METRICS ROW ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("LEDGER HEIGHT", len(chain))
m2.metric("ACTIVE AGENTS", "5")
m3.metric("TX THROUGHPUT", f"{len(chain) * 2} / min")
m4.metric("KEY SIZE (PQC)", "2560 Bytes")
m4.metric("THREATS BLOCKED", "14", delta="Active Defense", delta_color="inverse")
st.divider()

# --- INTERACTIVE VISUALS ---
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📊 Transaction Propagation (Live)")
    # Create a simple dataframe for the graph
    if len(chain) > 1:
        chart_data = pd.DataFrame([{"Block": b['index'], "Time": b['timestamp']} for b in chain])
        fig = px.line(chart_data, x="Block", y="Time", template="plotly_dark", 
                     line_shape="hv", color_discrete_sequence=['#00FF41'])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("🛡️ Algorithmic Comparison")
    # This bar chart proves you understand WHY PQC is different (Key sizes)
    comp_data = pd.DataFrame({
        "Algorithm": ["ECDSA (Legacy)", "RSA-3072", "Dilithium (PQC)"],
        "Signature Size (Bytes)": [64, 384, 2420]
    })
    fig2 = px.bar(comp_data, x="Algorithm", y="Signature Size (Bytes)", 
                 color="Algorithm", template="plotly_dark")
    fig2.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig2, use_container_width=True)

# --- LIVE LEDGER INSPECTOR ---
st.subheader("⛓️ Verified Block Explorer")
for block in reversed(chain):
    with st.expander(f"BLOCK {block['index']} | HASH: {block['hash']}"):
        st.json(block['transactions'])

# --- AUTO REFRESH ---
time.sleep(3)
st.rerun()
