import streamlit as st
from src.model import about_info

def show():
    st.header('Operating system')
    st.text(about_info.OS)
    st.header('Kernel')
    st.text(about_info.KERNEL)