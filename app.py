import streamlit as st
from firebase_auth import sign_up_user, sign_in_user

st.title("User Login / Sign Up")

menu = st.sidebar.selectbox("Choose", ["Login", "Sign Up"])

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if menu == "Sign Up":
    if st.button("Create Account"):
        result = sign_up_user(email, password)
        if "idToken" in result:
            st.success("User account created!")
        else:
            st.error(result.get("error", {}).get("message", "Signup failed"))

elif menu == "Login":
    if st.button("Login"):
        result = sign_in_user(email, password)
        if "idToken" in result:
            st.success(f"Welcome, {email}!")
            st.session_state["user_logged_in"] = True
            st.switch_page("pages/01 View Bin.py")
        else:
            st.error(result.get("error", {}).get("message", "Login failed"))
