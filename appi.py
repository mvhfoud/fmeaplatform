import streamlit as st
import time
import subprocess
import os


current_dir = os.path.dirname(os.path.abspath('appi.py'))
print(current_dir)

# Construct the path to your Streamlit app files
streamlit_app_path = os.path.join(current_dir, "client.py")


def authenticate(username, password):
    # Hardcoded username and password for demonstration purposes
    if username == "user" and password == "user":
        return 1
    if username == "admin" and password == "admin":
        return 2
    else:
        return 0

def main():
    st.title("Authentication Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(username, password)== 1:
            st.success("Logged in successfully! Client")
            time.sleep(2)
            try:
                process1 = subprocess.Popen(["streamlit", "run", streamlit_app_path])
            except subprocess.CalledProcessError as e:
                print(f"Oops an error occured! {e}")
        elif authenticate(username, password)== 2:
            st.success("Logged in successfully! Admin")
            time.sleep(2)
            # Redirect to another page or perform actions after successful login
            try:
                process1 = subprocess.Popen(["streamlit", "run", streamlit_app_path])
            except subprocess.CalledProcessError as e:
                print(f"Oops an error occured! {e}")
        else:
            st.error("Invalid username or password. Please try again.")

if __name__ == "__main__":
    main()
