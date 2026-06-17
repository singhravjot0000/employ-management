from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Employee
from app.schemas import EmployeeCreate
from app.auth import get_current_user

router = APIRouter(prefix="/employees", tags=["Employees"])



@router.post("/")
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    if user["role"] not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Not allowed")

    new_employee = Employee(**employee.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee

@router.get("/")
def get_all_employees(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    if user["role"] not in ["admin", "manager"]:
        raise HTTPException(status_code=403)

    return db.query(Employee).all()

@router.get("/{emp_id}")
def get_employee(
    emp_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    emp = db.query(Employee).filter(Employee.id == emp_id).first()

    if not emp:
        raise HTTPException(status_code=404)

    return emp

@router.delete("/{emp_id}")
def delete_employee(
    emp_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    if user["role"] != "admin":
        raise HTTPException(status_code=403)

    emp = db.query(Employee).filter(Employee.id == emp_id).first()

    if not emp:
        raise HTTPException(status_code=404)

    db.delete(emp)
    db.commit()

    return {"message": "Deleted"}

@router.put("/{emp_id}")
def update_employee(
    emp_id: int,
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    if user["role"] not in ["admin", "manager"]:
        raise HTTPException(status_code=403)

    emp = db.query(Employee).filter(Employee.id == emp_id).first()

    if not emp:
        raise HTTPException(status_code=404)

    for key, value in employee_data.dict().items():
        setattr(emp, key, value)

    db.commit()
    db.refresh(emp)

    return emp