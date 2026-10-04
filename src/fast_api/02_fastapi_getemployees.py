from fastapi import APIRouter
router = APIRouter()   
from fast_api.data_store import employees

@router.get("/employees")
def get_employees():
    return {"employees": employees}

@router.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    for employee in employees:
        if employee["id"] == employee_id:
            return {"employee": employee}
    return {"error": "Employee not found"}
