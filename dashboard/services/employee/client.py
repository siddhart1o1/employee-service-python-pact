import requests


class EmployeeServiceClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_all_employees(self):
        """Fetch all employees."""
        response = requests.get(f"{self.base_url}/employees")
        return response.json()

    def get_employee(self, employee_id):
        """Fetch a single employee by ID."""
        response = requests.get(f"{self.base_url}/employees/{employee_id}")
        return response.json()

    def add_employee(self, employee_data):
        """Add a new employee."""
        response = requests.post(f"{self.base_url}/employees", json=employee_data)
        return response.json()

    def update_employee(self, employee_id, employee_data):
        """Update an existing employee."""
        response = requests.put(
            f"{self.base_url}/employees/{employee_id}", json=employee_data
        )
        return response.json()

    def delete_employee(self, employee_id):
        """Delete an employee."""
        response = requests.delete(f"{self.base_url}/employees/{employee_id}")
        return response.ok

    def get_dashboard_data(self):
        """Fetch data for the dashboard"""
        response = requests.get(f"{self.base_url}/dashboard")
        return response.json()
