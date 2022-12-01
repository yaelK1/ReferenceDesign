import streamlit as st
def style():
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"]{
    background-color: #1D1C29;
    text-color: #FFFFFF;
    color: #FFFFFF;
    }
    div[data-baseweb="select"] {
        background-color: #36344B;
        }
    .stButton > button:first-child {
    background-color: #36344B;
    color: #B3B3B3;
    font-size: 10px;
    hight: 1em;
    width: 5em;
    border-radius: 5px 5px 5px 5px;
    }

    div.stButton > button:hover {
    background-color: #1D1C29;
    color:#B3B3B3;
    border-color: #B3B3B3;
    }

    div.stButton > button:focus {
    background-color: #1D1C29;
    color:#B3B3B3;
    border-color: #B3B3B3;
    box-shadow: none;
    }
    div.object-container {
    background-color: #1D1C29;
    }
    .stTextInput > div > input {
        color:#FFFFFF;
        text-color:#FFFFFF;
        }
    .stTextInput > label {
        color:#FFFFFF;
        }
    .stSelectbox > label {
        color:#FFFFFF;
        }   
    .stSubheader > label{
        color:#FFFFFF;
    }   
    iframe {background-color: #15151F;} 
     """,
    unsafe_allow_html=True)

