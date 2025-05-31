import streamlit as st

st.set_page_config(
    page_title="Dashboard • Diabetes & Nutrição",
    page_icon="🩺",
    layout="wide",
)

# Redireciona para a página principal
st.switch_page("pages/Dashboard.py")