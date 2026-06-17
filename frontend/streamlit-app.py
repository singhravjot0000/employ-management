import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/employees/"



st.title("Employee Management System 🚀")

# ---------------------------
# ADD EMPLOYEE
# ---------------------------
st.header("Add Employee")

first_name = st.text_input("First Name")
last_name = st.text_input("Last Name")
phone = st.text_input("Phone")
department = st.text_input("Department")
designation = st.text_input("Designation")
salary = st.number_input("Salary", step=1000)

if st.button("Add Employee"):
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone,
        "department": department,
        "designation": designation,
        "salary": salary,
        "joining_date": "2026-01-01",
        "user_id": 1
    }

    res = requests.post(API_URL, json=payload)

    if res.status_code in [200, 201]:
        st.success("Employee added successfully!")
    else:
        st.error(res.text)

# ---------------------------
# VIEW EMPLOYEES
# ---------------------------
st.header("All Employees")

if st.button("Load Employees"):
    res = requests.get(API_URL)
    employees = res.json()

    for emp in employees:
        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(f"""
            **ID:** {emp['id']}  
            **Name:** {emp['first_name']} {emp['last_name']}  
            **Phone:** {emp['phone']}  
            **designation:** {emp['designation']}                                                                     
            **Salary:** {emp['salary']}
            """)

        with col2:
            delete_btn = st.button("Delete", key=f"del_{emp['id']}")

            if delete_btn:
                url = f"{API_URL.rstrip('/')}/{emp['id']}"

                try:
                    del_res = requests.delete(url)

                    if del_res.status_code in [200, 204]:
                        st.success("Deleted successfully")
                         
                    else:
                        st.error(f"Delete failed: {del_res.status_code} - {del_res.text}")

                except Exception as e:
                    st.error(f"Request error: {e}")