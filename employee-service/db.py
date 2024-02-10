# mock_db.py

from typing import Dict, Optional
EMPLOYEES = {}


def get_employee(employee_id: int) -> Optional[Dict]:
    return EMPLOYEES.get(employee_id)


def get_all_employees() -> Dict[int, Dict]:
    return EMPLOYEES


def create_employee(employee: Dict) -> Dict:
    new_id = max(EMPLOYEES.keys(), default=0) + 1
    employee["employeeId"] = new_id
    EMPLOYEES[new_id] = employee
    return employee


def update_employee(employee_id: int, employee: Dict) -> Optional[Dict]:
    if employee_id in EMPLOYEES:
        EMPLOYEES[employee_id].update(employee)
        return EMPLOYEES[employee_id]
    return None


def delete_employee(employee_id: int) -> bool:
    if employee_id in EMPLOYEES:
        del EMPLOYEES[employee_id]
        return True
    return False


def reset_employees() -> None:
    EMPLOYEES.clear()
