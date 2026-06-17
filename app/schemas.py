from pydantic import BaseModel,EmailStr
from datetime import date

class UserCreate(BaseModel):
    username:str
    email:EmailStr
    password:str
    role:str="admin"
class UserResponse(BaseModel):
    id:int
    username:str
    email:EmailStr
    role:str
    
    class Config:
        from_attributes=True
        
class EmployeeCreate(BaseModel):
    user_id:int
    first_name:str
    last_name:str
    phone:str
    department:str
    designation:str
    joining_date:date
    salary:int

class EmployeeResponse(BaseModel):

    id:int
    first_name:str
    last_name:str
    phone:str
    designation:str
    salary:int
   


    class Config:
        from_attributes=True
        
class Login(BaseModel):

    email: EmailStr
    password: str
    