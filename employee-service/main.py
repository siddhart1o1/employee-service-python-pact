from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

import sys
from pathlib import Path

current_dir = Path(__file__).parent
sys.path.append(str(current_dir))


from db import (
    get_employee,
    get_all_employees,
    create_employee,
    update_employee,
    delete_employee,
)
from provider_states import get_setup_function_for_state

app = FastAPI()


class Employee(BaseModel):
    employeeId: Optional[int] = Field(None, alias="employeeId")
    name: str
    age: int
    department: str


class ProviderState(BaseModel):
    state: str
    params: dict


@app.post("/_pact/provider_states")
def setup_provider_state(provider_state: ProviderState):
    setup_function = get_setup_function_for_state(provider_state.state)
    if not setup_function:
        raise HTTPException(status_code=404, detail="Provider state function not found")
    setup_function()
    return {"status": "ok"}


@app.get("/employees", response_model=list[Employee])
def get_all():
    return list(get_all_employees().values())


@app.post("/employees", response_model=Employee)
def add_employee(employee: Employee):
    employee_data = employee.dict(exclude_unset=True)
    employee_data.pop("employeeId", None)
    created_employee = create_employee(employee_data)
    return created_employee


@app.get("/employees/{employee_id}", response_model=Employee)
def get(employee_id: int):
    employee = get_employee(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@app.put("/employees/{employee_id}", response_model=Employee)
def update(employee_id: int, employee: Employee):
    employee_data = employee.dict(exclude_unset=True)
    employee_data.pop("employeeId", None)
    updated_employee = update_employee(employee_id, employee_data)
    if not updated_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated_employee


@app.delete("/employees/{employee_id}")
def remove(employee_id: int):
    success = delete_employee(employee_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee removed"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
