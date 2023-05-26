from dao import user_dao
from db import conn
from fastapi.security import OAuth2PasswordRequestForm
from schemas import User, UserCreate
from sqlalchemy.orm import Session
from utilities import create_access_token, get_hashed_password, verify_password

from fastapi import APIRouter, Depends, HTTPException, status

from .deps import get_current_user

router = APIRouter(prefix="/users")


@router.get("/me", summary="Get details of currently user", response_model=User)
async def get_me(user: User = Depends(get_current_user)):
    return user


@router.post("/signup", summary="Create new user", response_model=User)
async def create_user(data: UserCreate, db: Session = Depends(conn)):
    # querying database to check if user already exist
    user = user_dao.get_by_field(db, "email", data.email)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist",
        )
    user_data = UserCreate(
        name=data.name,
        email=data.email,
        hashed_password=get_hashed_password(data.hashed_password),
    )
    user = user_dao.create(db, user_data)
    return user


@router.post(
    "/login", summary="Create access and refresh tokens for user", response_model=dict
)
async def login(
    data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(conn)
):
    user = user_dao.get_by_field(db, "email", data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    hashed_pass = user.hashed_password
    if not verify_password(data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    return {
        "access_token": create_access_token(user.email),
    }
