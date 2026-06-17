from sqlalchemy import Column,Integer,String,Date,ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)   
    username=Column(String,unique=True)
    email=Column(String,unique=True)
    password=Column(String)
    role=Column(String,default="admin")
    employee = relationship("Employee", back_populates="user", uselist=False)
    
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String, unique=True, index=True)

    department = Column(String, nullable=False)
    designation = Column(String, nullable=False)

    joining_date = Column(Date, nullable=False)

    salary = Column(Integer, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship with User table
    user = relationship("User", back_populates="employee")


    