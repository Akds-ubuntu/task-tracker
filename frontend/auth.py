import streamlit as st


def show_login(api):
    st.title("🔐 Вход")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Пароль", type="password")
        submit = st.form_submit_button("Войти")

        if submit:
            if email and password:
                try:
                    with st.spinner("Вход..."):
                        response = api.login(email, password)
                    if response.status_code == 200:
                        st.success("✅ Успешный вход!")
                        st.rerun()
                    else:
                        error_detail = response.json().get('detail', 'Неизвестная ошибка')
                        st.error(f"❌ Ошибка входа: {error_detail}")
                except Exception as e:
                    st.error(f"❌ Ошибка подключения: {e}")
            else:
                st.warning("⚠️ Заполните все поля")


def show_register(api):
    st.title("📝 Регистрация")

    with st.form("register_form"):
        username = st.text_input("Имя пользователя")
        email = st.text_input("Email")
        password = st.text_input("Пароль", type="password")
        submit = st.form_submit_button("Зарегистрироваться")

        if submit:
            if username and email and password:
                try:
                    with st.spinner("Регистрация..."):
                        response = api.register(username, email, password)
                    if response.status_code == 200:
                        st.success("✅ Регистрация успешна!")
                        with st.spinner('Вход'):
                            login_response = api.login(email, password)
                        if response.status_code == 200:
                            st.success("✅ Успешный вход!")
                            st.rerun()
                        else:
                            error_detail = login_response.json().get('detail','Неизвестная ошибка')
                            st.error(f"❌ Регистрация успешна, но вход не удался: {error_detail}")
                    else:
                        error_detail = response.json().get('detail', 'Неизвестная ошибка')
                        st.error(f"❌ Ошибка регистрации: {error_detail}")
                except Exception as e:
                    st.error(f"❌ Ошибка подключения: {e}")
            else:
                st.warning("⚠️ Заполните все поля")


def show_profile(api):
    col1, col2 = st.columns([3, 1])

    with col1:
        st.title("👤 Профиль")
        try:
            with st.spinner("Зашрузка..."):
                response = api.get_me()
            if response.status_code == 200:
                user = response.json()
                st.write(f"**Username:** {user['username']}")
                st.write(f"**Email:** {user['email']}")
                st.write(f"**ID:** {user['id']}")
            else:
                st.error("❌ Ошибка загрузки профиля")
        except Exception as e:
            st.error(f"❌ Ошибка подключения: {e}")
    with col2:
        st.write("")
        st.write("")
        if st.button("🚪 Выйти"):
            try:
                api.logout()
                st.rerun()
            except Exception as e:
                st.error(f"❌ Ошибка выхода: {e}")
