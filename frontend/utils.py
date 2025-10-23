import requests
import streamlit as st


class API:
    def __init__(self, base_url):
        self.base_url = base_url

    def _get_headers(self):
        token = st.session_state.get('token')
        return {'Authorization': f'Bearer {token}'} if token else {}

    def register(self, username, email, password):
        url = f"{self.base_url}/api/register"
        data = {"username": username, "email": email, "password": password}
        return requests.post(url, json=data)

    def login(self, email, password):
        url = f"{self.base_url}/api/login"
        data = {"email": email, "password": password}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            st.session_state.token = response.json()['access_token']
        return response

    def get_me(self):
        url = f"{self.base_url}/api/me"
        return requests.get(url, headers=self._get_headers())

    def logout(self):
        url = f"{self.base_url}/api/logout"
        response = requests.post(url, headers=self._get_headers())
        if response.status_code == 200:
            st.session_state.token = None
        return response
