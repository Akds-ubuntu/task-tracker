import os

import streamlit as st


def get_backend_url():
    try:
        return st.secrets["BACKEND_URL"]
    except (KeyError, FileNotFoundError):
        env_url = os.getenv("BACKEND_URL")
        if env_url:
            return env_url
        return "http://localhost:8000"

API_BASE_URL = get_backend_url()


def setup_page():
    st.set_page_config(
        page_title="Task Tracker",
        page_icon="✅",
        layout="wide"
    )
