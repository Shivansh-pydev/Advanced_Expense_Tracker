import streamlit as st

USER = "admin"
PASS = "1234"

def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("🔐 Login Required")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username == USER and password == PASS:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials")
        return False

    return True
