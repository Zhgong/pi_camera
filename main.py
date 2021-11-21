import streamlit as st
import pandas as pd
import numpy as np
from src.view import about

st.title('RTSP Camera with Raspberry Pi')
st.sidebar.title("Navigation")

nav = st.sidebar.radio("Choose a tab",('Camera', 'About'))

if nav == "About":
    
    about.show()
