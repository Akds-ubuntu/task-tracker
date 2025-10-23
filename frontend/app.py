import streamlit as st

from auth import show_login, show_register, show_profile
from config import setup_page, API_BASE_URL
from utils import API


def main():
    setup_page()
    if 'api' not in st.session_state:
        st.session_state.api = API(API_BASE_URL)
    if 'token' not in st.session_state:
        st.session_state.token = None

    api = st.session_state.api

    if not st.session_state.token:
        tab1, tab2 = st.tabs(["🔐 Вход", "📝 Регистрация"])

        with tab1:
            show_login(api)

        with tab2:
            show_register(api)
    else:
        show_profile(api)


if __name__ == "__main__":
    main()
