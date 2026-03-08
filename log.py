import streamlit as st
import hashlib

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load credentials from file
def load_credentials(filename):
    credentials = {}
    with open(filename, 'r') as f:
        for line in f:
            username, password = line.strip().split(',')
            credentials[username] = password.strip()
    return credentials

# Function to run the Streamlit app
def run_app():
    # Initialize session state for login status
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    # Load credentials from file
    credentials = load_credentials('credentials.txt')

    # Login form
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        hashed_password = hash_password(password)
        if username in credentials and credentials[username] == hashed_password:
            st.session_state['logged_in'] = True
            st.success("Login successful!")

            # Provide a clickable link to the AI_Chatbot page
            chatbot_url = "https://064f0a6de65be1f8469132c6995a5527.serveo.net"  # Replace with your actual chatbot URL
            st.markdown(f"Click [here]({chatbot_url}) to access the AI-Studybot.")
        else:
            st.error("Invalid username or password")

run_app()