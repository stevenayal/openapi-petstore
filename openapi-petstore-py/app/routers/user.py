from datetime import datetime, timezone, timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserSchema

router = APIRouter(tags=["user"])


def _user_to_schema(user: User) -> UserSchema:
    return UserSchema(
        id=user.id,
        username=user.username,
        firstName=user.first_name,
        lastName=user.last_name,
        email=user.email,
        password=user.password,
        phone=user.phone,
        userStatus=user.user_status,
    )


@router.post(
    "/user",
    summary="Create user",
    operation_id="createUser",
    response_model=UserSchema,
    response_model_by_alias=True,
    responses={"default": {"description": "successful operation"}},
)
def create_user(
    user_data: UserSchema,
    db: Session = Depends(get_db),
):
    existing = db.query(User).filter(User.username == user_data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(
        username=user_data.username,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        password=user_data.password,
        phone=user_data.phone,
        user_status=user_data.user_status or 0,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return _user_to_schema(user)


@router.post(
    "/user/createWithArray",
    summary="Creates list of users with given input array",
    operation_id="createUsersWithArrayInput",
    responses={"default": {"description": "successful operation"}},
)
def create_users_with_array(
    users: List[UserSchema],
    db: Session = Depends(get_db),
):
    for u in users:
        user = User(
            username=u.username,
            first_name=u.first_name,
            last_name=u.last_name,
            email=u.email,
            password=u.password,
            phone=u.phone,
            user_status=u.user_status or 0,
        )
        db.add(user)
    db.commit()
    return {"message": "Users created successfully"}


@router.post(
    "/user/createWithList",
    summary="Creates list of users with given input array",
    operation_id="createUsersWithListInput",
    responses={"default": {"description": "successful operation"}},
)
def create_users_with_list(
    users: List[UserSchema],
    db: Session = Depends(get_db),
):
    return create_users_with_array(users, db)


@router.get(
    "/user/login",
    summary="Logs user into the system",
    operation_id="loginUser",
    responses={
        200: {"description": "successful operation"},
        400: {"description": "Invalid username/password supplied"},
    },
)
def login_user(
    username: str = Query(..., description="The user name for login"),
    password: str = Query(..., description="The password for login"),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    expires = datetime.now(timezone.utc) + timedelta(hours=1)
    return Response(
        content=f"Logged in user session: {int(expires.timestamp())}",
        media_type="application/json",
        headers={
            "X-Rate-Limit": "5000",
            "X-Expires-After": expires.isoformat(),
        },
    )


@router.get(
    "/user/logout",
    summary="Logs out current logged in user session",
    operation_id="logoutUser",
    responses={"default": {"description": "successful operation"}},
)
def logout_user():
    return {"message": "User logged out successfully"}


@router.get(
    "/user/{username}",
    summary="Get user by user name",
    operation_id="getUserByName",
    response_model=UserSchema,
    response_model_by_alias=True,
    responses={
        200: {"description": "successful operation"},
        400: {"description": "Invalid username supplied"},
        404: {"description": "User not found"},
    },
)
def get_user_by_name(
    username: str,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return _user_to_schema(user)


@router.put(
    "/user/{username}",
    summary="Updated user",
    operation_id="updateUser",
    response_model=UserSchema,
    response_model_by_alias=True,
    responses={
        400: {"description": "Invalid user supplied"},
        404: {"description": "User not found"},
    },
)
def update_user(
    username: str,
    user_data: UserSchema,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_data.first_name is not None:
        user.first_name = user_data.first_name
    if user_data.last_name is not None:
        user.last_name = user_data.last_name
    if user_data.email is not None:
        user.email = user_data.email
    if user_data.password is not None:
        user.password = user_data.password
    if user_data.phone is not None:
        user.phone = user_data.phone
    if user_data.user_status is not None:
        user.user_status = user_data.user_status
    db.commit()
    db.refresh(user)
    return _user_to_schema(user)


@router.delete(
    "/user/{username}",
    summary="Delete user",
    operation_id="deleteUser",
    responses={
        400: {"description": "Invalid username supplied"},
        404: {"description": "User not found"},
    },
)
def delete_user(
    username: str,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
