import json
from dashboard.services.employee.client import EmployeeServiceClient
from pact import Consumer, Like, Provider, Term
import os
import pytest

PACT_FILE = "employee-service.json"
PACT_MOCK_HOST = "localhost"
PACT_MOCK_PORT = 1234
PACT_DIR = (
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    + "/pact"
)


@pytest.fixture
def client():
    return EmployeeServiceClient(f"http://{PACT_MOCK_HOST}:{PACT_MOCK_PORT}")


@pytest.fixture(scope="session")
def pact(request):
    pact = Consumer("Dashboard").has_pact_with(
        Provider("EmployeeService"),
        host_name=PACT_MOCK_HOST,
        port=PACT_MOCK_PORT,
        pact_dir=PACT_DIR,
    )
    pact.start_service()
    yield pact
    pact.stop_service()


def test_add_employee(client, pact):
    new_employee = {
        "name": "Siddharth Tiwari",
        "age": 21,
        "department": "Software Engineering",
    }
    expected = {"employeeId": Like(1), **new_employee}

    pact.given("Adding a new employee").upon_receiving(
        "A request to add a new employee"
    ).with_request(
        "post",
        "/employees",
        body=new_employee,
        headers={"Content-Type": "application/json"},
    ).will_respond_with(
        200,
        body=Like(expected),
    )

    with pact:
        client.add_employee(new_employee)


def test_get_all_employees(client, pact):
    expected = [
        {
            "employeeId": Like(1),
            "name": "Siddharth Tiwari",
            "age": 21,
            "department": "Software Engineering",
        },
        {
            "employeeId": Like(1),
            "name": "Alice Doe",
            "age": 25,
            "department": "Software Engineering",
        },
    ]

    pact.given("Employees exist").upon_receiving(
        "A request for all employees"
    ).with_request("get", "/employees").will_respond_with(200, body=Like(expected))

    with pact:
        client.get_all_employees()


def test_get_employee(client, pact):
    expected = {
        "employeeId": Like(1),
        "name": "Siddharth Tiwari",
        "age": 21,
        "department": "Software Engineering",
    }

    pact.given("Employee with ID 1 exists").upon_receiving(
        "A request for employee with ID 1"
    ).with_request("get", "/employees/1").will_respond_with(200, body=Like(expected))

    with pact:
        client.get_employee(1)


def test_update_employee(client, pact):
    employee_id = 1
    employee_update = {
        "name": "Siddharth Tiwari",
        "age": 29,
        "department": "Human Resources",
    }
    expected = {"employeeId": Like(1), **employee_update}

    pact.given("Employee with ID 1 can be updated").upon_receiving(
        "A request to update employee with ID 1"
    ).with_request(
        "put",
        f"/employees/{employee_id}",
        body=employee_update,
        headers={"Content-Type": "application/json"},
    ).will_respond_with(
        200,
        body=Like(expected),
    )

    with pact:
        client.update_employee(employee_id, employee_update)


def test_delete_employee(client, pact):
    pact.given("Employee with ID 1 exists and can be deleted").upon_receiving(
        "A request to delete employee with ID 1"
    ).with_request("delete", "/employees/1").will_respond_with(200)

    with pact:
        client.delete_employee(1)
