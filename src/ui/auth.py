import streamlit as st
import hashlib

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"] == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        st.button("Login", on_click=password_entered)
        return False
    
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        st.button("Login", on_click=password_entered)
        st.error("😕 User not known or password incorrect")
        return False
    
    else:
        # Password correct.
        return True

def simple_login():
    """A simpler login for demonstration without secrets.toml dependency for this artifacts run."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        return True

    st.markdown("## 🔐 Access Control")
    st.markdown("Please sign in to access the Security Dashboard.")
    
    # Styled Login Box
    with st.container():
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.button("Login")
            
    if login_btn:
        if username == "admin" and password == "admin":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials. Try admin/admin")
            
    return False
