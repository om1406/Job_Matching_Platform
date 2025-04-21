import streamlit as st
from user_auth import init_db, register_user, login_user, get_all_users, add_job, get_jobs, update_profile, change_password

init_db()

if 'user' not in st.session_state:
    st.session_state.user = None

def show_login():
    st.title("Login / Register")
    option = st.radio("Choose an option", ("Login", "Register"))

    if option == "Login":
        email = st.text_input("Email")
        password = st.text_input("Password", type='password')
        if st.button("Login"):
            user = login_user(email, password)
            if user:
                st.success(f"Welcome {user[1]}!")
                st.session_state.user = {
                    'id': user[0],
                    'name': user[1],
                    'email': user[2],
                    'is_admin': bool(user[4])
                }
                st.experimental_rerun()
            else:
                st.error("Invalid credentials")

    else:
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type='password')
        is_admin = st.checkbox("Register as Admin")
        if st.button("Register"):
            success = register_user(name, email, password, is_admin)
            if success:
                st.success("Registered! Please log in.")
            else:
                st.error("Email already exists.")

def admin_dashboard():
    st.subheader("👥 All Registered Users")
    users = get_all_users()
    for user in users:
        st.write(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Admin: {'Yes' if user[3] else 'No'}")

    st.subheader("📄 Post a New Job")
    title = st.text_input("Job Title")
    desc = st.text_area("Job Description")
    if st.button("Add Job"):
        add_job(title, desc)
        st.success("Job posted!")

def user_dashboard():
    st.subheader("📝 Job Listings")
    jobs = get_jobs()
    for job in jobs:
        st.markdown(f"**{job[1]}**\n\n{job[2]}\n---")

    st.subheader("🔧 Edit Profile")
    name = st.text_input("Update Name", value=st.session_state.user['name'])
    email = st.text_input("Update Email", value=st.session_state.user['email'])
    if st.button("Update Profile"):
        success = update_profile(st.session_state.user['id'], name, email)
        if success:
            st.success("Profile updated!")
            st.session_state.user['name'] = name
            st.session_state.user['email'] = email
        else:
            st.error("Email already in use.")

    st.subheader("🔒 Change Password")
    new_pw = st.text_input("New Password", type='password')
    if st.button("Change Password"):
        change_password(st.session_state.user['id'], new_pw)
        st.success("Password changed!")

def main():
    if st.session_state.user is None:
        show_login()
    else:
        st.sidebar.success(f"Logged in as {st.session_state.user['name']}")
        if st.sidebar.button("Logout"):
            st.session_state.user = None
            st.experimental_rerun()

        if st.session_state.user['is_admin']:
            st.title("🔐 Admin Dashboard")
            admin_dashboard()
        else:
            st.title("🎯 Job Matching Platform")
            user_dashboard()

main()
