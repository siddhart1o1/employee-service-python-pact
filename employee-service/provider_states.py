# provider_states.py

from db import reset_employees, create_employee


def reset_states():
    reset_employees()


def setup_user_Siddharth():
    reset_states()
    create_employee(
        {"name": "Siddharth Tiwari", "age": 21, "department": "Software Engineering"}
    )


def setup_user_alice():
    create_employee(
        {
            "name": "Alice Doe",
            "age": 25,
            "department": "Software Engineering",
        }
    )


def setup_employees():
    setup_user_Siddharth()
    setup_user_alice()


STATE_SETUP_FUNCTIONS = {
    "Adding a new employee": reset_states,
    "Employees exist": setup_employees,
    "Employee with ID 1 exists": setup_user_Siddharth,
    "Employee with ID 1 can be updated": setup_user_Siddharth,
    "Employee with ID 1 exists and can be deleted": setup_user_Siddharth,
}


def get_setup_function_for_state(state_name: str):
    return STATE_SETUP_FUNCTIONS.get(state_name)
