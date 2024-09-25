import streamlit as st
import os
import json
import pandas as pd
import plotly.express as px
 
# Define file paths
user_data_file = 'users.json'
 
# Load user data from JSON
def load_user_data():
    if os.path.exists(user_data_file):
        with open(user_data_file, 'r') as f:
            return json.load(f)
    else:
        return {}
 
# Save user data to JSON
def save_user_data(data):
    with open(user_data_file, 'w') as f:
        json.dump(data, f, indent=4)
 
# Function to create a user directory
def create_user_directory(email):
    user_dir = os.path.join(os.getcwd(), email)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    return user_dir
 
# Function to validate sign up
def validate_signup(email, users):
    if email in users:
        return False, "Email already exists!"
    return True, ""
 
# Function to validate login
def validate_login(email, password, users):
    if email in users and users[email]["password"] == password:
        return True, ""
    elif email not in users:
        return False, "Email does not exist!"
    else:
        return False, "Incorrect password!"
 
# Load existing user data
users = load_user_data()
 
# Sidebar for login and signup
st.sidebar.title("Authentication")
page = st.sidebar.radio("Go to", ["Login", "Sign Up"])

# If the user is logged in, show the sign-out button in the sidebar
if st.session_state.get("logged_in", False):
    if st.sidebar.button("Sign Out"):
        st.session_state["logged_in"] = False
        st.session_state["user_email"] = None
        st.success("You have been signed out!")
 
if page == "Sign Up":
    st.title("Welcome to the Sign Up Page")
 
    # Input fields for signup
    name = st.text_input("Name")
    phone = st.text_input("Phone")
    dob = st.date_input("DOB")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
 
    if st.button("Sign Up"):
        # Validate signup details
        is_valid, message = validate_signup(email, users)
        if not is_valid:
            st.error(message)
        else:
            # Store user data in JSON
            users[email] = {
                "name": name,
                "phone": phone,
                "dob": str(dob),
                "password": password,
            }
            save_user_data(users)
           
            # Create user directory
            create_user_directory(email)
           
            st.success("Sign up successful! Please login.")
 
elif page == "Login":
    st.title("Welcome to the Login Page")
 
    # Input fields for login
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
 
    if st.button("Login"):
        is_valid, message = validate_login(email, password, users)
        if not is_valid:
            st.error(message)
        else:
            st.success(f"Welcome, {users[email]['name']}!")
            st.session_state["logged_in"] = True
            st.session_state["user_email"] = email
 
# If the user is logged in, move to marks submission
if st.session_state.get("logged_in", False):
    st.title(f"Welcome {users[st.session_state['user_email']]['name']}")
 
    # Marks input for 7 subjects
    subjects = ["Math", "English", "Science", "History", "Geography", "Art", "PE"]
    marks = []
    for subject in subjects:
        mark = st.slider(f"Choose your marks for {subject}", 0, 100)
        marks.append(mark)
 
    if st.button("Submit Marks"):
        user_dir = create_user_directory(st.session_state["user_email"])
        marks_file = os.path.join(user_dir, "marks.csv")
       
        # Save marks to CSV
        marks_df = pd.DataFrame({"Subject": subjects, "Marks": marks})
        marks_df.to_csv(marks_file, index=False)
       
        st.success("Marks submitted successfully!")
 
        # Generate reports
        st.title("Your Reports are Ready!")
 
        # Bar graph for average marks
        st.subheader("Average Marks Chart (Bar Graph)")
        avg_marks = pd.DataFrame({"Subject": subjects, "Marks": marks})
        bar_fig = px.bar(avg_marks, x="Subject", y="Marks")
        st.plotly_chart(bar_fig)
 
        # Line graph for marks per subject
        st.subheader("Marks as per each subject (Line Graph)")
        line_fig = px.line(avg_marks, x="Subject", y="Marks")
        st.plotly_chart(line_fig)
 
        # Pie chart for marks distribution
        st.subheader("Marks as per each subject (Pie Chart)")
        pie_fig = px.pie(avg_marks, names="Subject", values="Marks")
        st.plotly_chart(pie_fig)
