
import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv
import altair as alt

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000")
st.set_page_config(page_title="Zeta", page_icon="⚛️", layout="wide")

st.title("⚛️ Zeta")
st.markdown("**Autonomous QA Architect & Physics Engine**")

tab1, tab2, tab3, tab4 = st.tabs(["📝 Generate", "🧪 Cases", "💻 Code", "📊 Analytics"])

if 'test_suite' not in st.session_state:
    st.session_state['test_suite'] = None
if 'selected_case' not in st.session_state:
    st.session_state['selected_case'] = None

# TAB 1
with tab1:
    req_text = st.text_area("Requirements", height=300)
    if st.button("🚀 Generate"):
        with st.spinner("Zeta is calculating Z-Scores..."):
            try:
                resp = requests.post(f"{API_URL}/generate", json={"requirements_text": req_text})
                if resp.status_code == 200:
                    st.session_state['test_suite'] = resp.json()
                    st.success("Generated!")
                else:
                    st.error(resp.text)
            except Exception as e:
                st.error(f"Error: {e}")

# TAB 2
with tab2:
    if st.session_state['test_suite']:
        cases = st.session_state['test_suite'].get("test_cases", [])
        for tc in cases:
            title = tc.get('title') or tc.get('name') or "Untitled"
            type_ = tc.get('type') or "Unknown"
            
            with st.expander(f"{title} ({type_})"):
                st.write(tc.get('steps', []))
                if st.button("Select", key=tc.get('id', '0')):
                    st.session_state['selected_case'] = tc
                    st.toast("Selected!")

# TAB 3
with tab3:
    if st.session_state['selected_case']:
        if st.button("Generate Code"):
            resp = requests.post(f"{API_URL}/codegen", json={"test_plan": st.session_state['selected_case']})
            if resp.status_code == 200:
                st.code(resp.json()['python_code'], language='python')

# TAB 4 - Restored Analytics (Using Pandas/Altair)
with tab4:
    if st.session_state['test_suite']:
        cases = st.session_state['test_suite'].get("test_cases", [])
        
        # Metrics
        total = len(cases)
        edge_cases = sum(1 for c in cases if c.get('risk_analysis', {}).get('is_edge_case'))
        
        c1, c2 = st.columns(2)
        c1.metric("Total Tests", total)
        c2.metric("Critical Edge Cases", edge_cases)
        
        # Chart
        data = []
        for c in cases:
            data.append({
                "ID": c.get('id', 'Unknown'),
                "Complexity": c.get('risk_analysis', {}).get('complexity_score', 0)
            })
        
        if data:
            df = pd.DataFrame(data)
            chart = alt.Chart(df).mark_bar().encode(
                x='ID',
                y='Complexity',
                tooltip=['ID', 'Complexity']
            ).properties(title="Requirement Entropy (Z-Score)")
            st.altair_chart(chart, use_container_width=True)
