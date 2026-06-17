from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.database import get_db
from app.models import User
from app.schemas import UserCreate

from app.auth import (hash_password,verify_password,create_token)


router = APIRouter(prefix="/users",tags=["Users"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(User).filter(
        User.email == user.email
    ).first()


    if existing:
        raise HTTPException(
            400,
            "Email already exists"
        )


    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )


    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return {
        "message":"User created"
    }



@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    
    db_user = db.query(User).filter(
        User.email == form_data.username
    ).first()


    if not db_user:
        raise HTTPException(
            404,
            "User not found"
        )


    if not verify_password(
        form_data.password,
        db_user.password
    ):
        raise HTTPException(
            401,
            "Wrong password"
        )


     
    token = create_token({
        "sub": db_user.email,
        "role": db_user.role
    })



    return {
        "access_token": token,
        "token_type": "bearer"
    }




@router.get("/profile")
def profile(user=Depends(get_current_user), db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user["email"]).first()

    return {
        "id": db_user.id,
        "username": db_user.username,
        "email": db_user.email,
        "role": db_user.role
    }
 
@router.put("/{emp_id}", response_model=UserCreate)
def update_user(
    emp_id: int,
    user_data: UserCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    if user["role"] != "admin":
        raise HTTPException(status_code=403)

    db_user = db.query(User).filter(User.id == emp_id).first()

    if not db_user:
        raise HTTPException(status_code=404)

    for key, value in user_data.dict().items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    return {
        "message": "User updated"
    }




 