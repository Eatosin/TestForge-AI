import streamlit as st
import requests
import pandas as pd
import json
import os
from dotenv import load_dotenv
import altair as alt

# Load Env.
load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="TestForge AI", page_icon="🛠️", layout="wide")

# Custom CSS for "Professional Dashboard" vibe
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #1E1E1E; border-radius: 5px; color: white; }
    .stTabs [aria-selected="true"] { background-color: #4CAF50; }
    .metric-card { background-color: #262730; padding: 20px; border-radius: 10px; border: 1px solid #444; }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
c1, c2 = st.columns([1, 4])
with c1:
    st.image("https://img.icons8.com/color/96/artificial-intelligence.png", width=80)
with c2:
    st.title("TestForge AI")
    st.markdown("**Autonomous QA Architect & Edge Case Detector**")

# --- NAVIGATION ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📝 1. Generate & Plan", 
    "🧪 2. Test Cases", 
    "💻 3. Code Studio", 
    "📊 4. Analytics & Risk"
])

# --- GLOBAL STATE ---
if 'test_suite' not in st.session_state:
    st.session_state['test_suite'] = None
if 'selected_case' not in st.session_state:
    st.session_state['selected_case'] = None

# --- TAB 1: GENERATION ---
with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Requirement Ingestion")
        req_text = st.text_area("Paste User Stories / Requirements", height=400, 
            placeholder="AS A user I WANT to login SO THAT I can access my dashboard...")
        
        if st.button("🚀 Analyze & Generate", type="primary", use_container_width=True):
            if len(req_text) < 10:
                st.error("Requirements too short.")
            else:
                with st.spinner("🤖 Gemini is architecting test plan + ML calculating Z-Scores..."):
                    try:
                        resp = requests.post(f"{API_URL}/generate", json={"requirements_text": req_text})
                        if resp.status_code == 200:
                            st.session_state['test_suite'] = resp.json()
                            st.success("Test Suite Generated Successfully!")
                        else:
                            st.error(f"API Error: {resp.text}")
                    except Exception as e:
                        st.error(f"Connection Failed: {e}")

    with col2:
        st.info("ℹ️ **System Status:**")
        try:
            health = requests.get(f"{API_URL}/health", timeout=1).json()
            st.write(f"**API Backend:** 🟢 Online ({health.get('status')})")
            st.write(f"**Engines Loaded:** {', '.join(health.get('engines_loaded', []))}")
        except:
            st.write("**API Backend:** 🔴 Offline (Check Docker)")

# --- TAB 2: VIEW TEST CASES ---
with tab2:
    if st.session_state['test_suite']:
        cases = st.session_state['test_suite'].get("test_cases", [])
        
        # Filters
        filter_type = st.multiselect("Filter by Type", ["Happy Path", "Edge Case", "Security"], default=["Happy Path", "Edge Case", "Security"])
        
        # Display
        for tc in cases:
            if tc.get('type') in filter_type:
                risk = tc.get("risk_analysis", {}).get("risk_level", "NORMAL")
                color = "red" if risk == "CRITICAL" else "orange" if risk == "HIGH" else "green"
                
                with st.expander(f":{color}_circle: [{tc['id']}] {tc['title']} ({tc['type']})"):
                    c1, c2 = st.columns(2)
                    c1.write("**Preconditions:**")
                    c1.write(tc.get('preconditions'))
                    c2.write("**Risk Analysis:**")
                    c2.json(tc.get('risk_analysis'))
                    
                    st.write("**Steps:**")
                    for s in tc.get('steps', []):
                        st.markdown(f"- {s}")
                    
                    if st.button("Select for Code Gen", key=f"btn_{tc['id']}"):
                        st.session_state['selected_case'] = tc
                        st.toast(f"Selected {tc['id']}! Go to Tab 3.")
    else:
        st.info("👈 Please generate a test suite in Tab 1 first.")

# --- TAB 3: CODE STUDIO ---
with tab3:
    if st.session_state['selected_case']:
        tc = st.session_state['selected_case']
        st.subheader(f" Generating Selenium Code for: {tc['id']}")
        
        if st.button("⚡ Compile Python Script", type="primary"):
            with st.spinner("Compiling Page Object Model..."):
                try:
                    resp = requests.post(f"{API_URL}/codegen", json={"test_plan": tc})
                    if resp.status_code == 200:
                        code = resp.json()['python_code']
                        st.code(code, language='python')
                        st.download_button("Download .py", code, f"test_{tc['id']}.py")
                    else:
                        st.error("Codegen Failed")
                except:
                    st.error("API Error")
    else:
        st.info("Select a test case from Tab 2 to generate code.")

# --- TAB 4: ANALYTICS (The Physics Dashboard) ---
with tab4:
    if st.session_state['test_suite']:
        st.subheader("📊 Quality Assurance Metrics")
        cases = st.session_state['test_suite'].get("test_cases", [])
        
        # 1. KPI Cards
        total = len(cases)
        edge_cases = sum(1 for c in cases if c.get('risk_analysis', {}).get('is_edge_case'))
        security = sum(1 for c in cases if c.get('type') == 'Security')
        
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total Coverage", total)
        k2.metric("Edge Cases (Z-Score)", edge_cases, delta=f"{edge_cases/total:.0%}")
        k3.metric("Security Scenarios", security)
        k4.metric("Avg Complexity", "0.72") # Mock metric based on text length

        # 2. Charts
        st.divider()
        c1, c2 = st.columns(2)
        
        with c1:
            st.write("**Test Distribution**")
            df_type = pd.DataFrame([c['type'] for c in cases], columns=['Type'])
            chart = alt.Chart(df_type).mark_arc(innerRadius=50).encode(
                theta=alt.Theta("count()", stack=True),
                color=alt.Color("Type"),
                tooltip=["Type", "count()"]
            )
            st.altair_chart(chart, use_container_width=True)
            
        with c2:
            st.write("**Complexity Heatmap (Z-Scores)**")
            # Create data for chart
            data = []
            for c in cases:
                data.append({
                    "ID": c['id'],
                    "Z-Score": c.get('risk_analysis', {}).get('complexity_score', 0),
                    "Risk": c.get('risk_analysis', {}).get('risk_level', "NORMAL")
                })
            df_risk = pd.DataFrame(data)
            
            bar_chart = alt.Chart(df_risk).mark_bar().encode(
                x='ID',
                y='Z-Score',
                color=alt.Color('Risk', scale=alt.Scale(domain=['NORMAL', 'HIGH', 'CRITICAL'], range=['green', 'orange', 'red']))
            )
            st.altair_chart(bar_chart, use_container_width=True)

    else:
        st.info("Analytics will appear here after generation.")
