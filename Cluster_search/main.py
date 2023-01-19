import streamlit as st
import oneai
import os
import sys
import webbrowser
import asyncio
import streamlit.components.v1 as components
from design import *
import requests
import json


def find_clusters(collection_name, api_key, search_text, uri):
    url = f"{uri}/clustering/v1/collections/{collection_name}/clusters/find?multilingual=true&translate=true&similarity_threshold=0.5&text={search_text}"
    headerrs = {"api-key": api_key}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.text()


def start_loader():
    envierment = st.selectbox("Select Enviroment", ("Prod", "Staging"))
    api_key = st.text_input("Enter API Key")
    if envierment == "Prod":
        uri = "https://api.oneai.com"
    if envierment == "Staging":
        uri = "https://staging.oneai.com"
    collection_name = st.text_input("Enter Collection Name")
    search_text = st.text_input("Enter Search Text")
    if st.button("Find Clusters"):
        clusters = find_clusters(collection_name, api_key, search_text, uri)
        st.write(clusters)
        st.stop()

