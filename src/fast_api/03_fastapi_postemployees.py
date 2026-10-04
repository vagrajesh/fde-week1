from fastapi import APIRouter
from fast_api.data_store import employees
from pydantic import BaseModel
from fast_api.model import Employee

router = APIRouter()

@router.post("/employees")
def add_employee(employee: Employee):
    new_employee = employee.model_dump()
    employee_id = len(employees) + 1
    employee.id = employee_id
    employees.append(new_employee)
    return {"employee": new_employee}