from fastapi import FastAPI, Depends, HTTPException
from app.database import engine, Base
from app import models  
from app.routers import users,employees
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import EmployeeResponse
 


Base.metadata.create_all(bind=engine)




app = FastAPI(
    title="Employment Management System",
    version="1.0.0",
)   

# here i have included the routers for users and employees, which will handle the respective endpoints for user registration, login, and employee management. The home endpoint is a simple GET request that returns a welcome message when the API is accessed at the root URL.
app.include_router(users.router)
app.include_router(employees.router)


