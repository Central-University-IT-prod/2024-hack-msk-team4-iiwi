from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from app import ALGORITHM, SECURITY_KEY, projectConfig
from app.data.errors import Errors
from app.data.models import AdminFront, TokenData
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

context_pass = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth_bearer = OAuth2PasswordBearer(
    tokenUrl=f"/token/new"
)


def verify_password(plain_password, hashed_password):
    """
    Verify if the provided plain password matches the hashed password.

    Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return context_pass.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Hash the provided password using bcrypt.

    Args:
        password (str): The plain text password.

    Returns:
        str: The hashed password.
    """
    return context_pass.hash(password)


async def authenticate_user(username: str, password: str):
    """
    Authenticate the user by verifying the username and password.

    Args:
        username (str): The username of the user.
        password (str): The plain text password of the user.

    Returns:
        AdminFront (bool): The user object if authentication is successful, False otherwise.
    """
    #TODO: Handle existans of admin user in Mongo
    print(username)
    users = await AdminFront.find_all().to_list()
    print(users)
    user = await AdminFront.find(AdminFront.username == username, fetch_links=True).to_list()
    print(user)
    hashed_instance = await user[0].secret.fetch()
    if not user:
        return False
    if not verify_password(password, hashed_instance.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create a JWT access token.

    Args:
        data (dict): The data to encode in the token.
        expires_delta (timedelta | None): The expiration time delta for the token. Defaults to 15 minutes.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECURITY_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth_bearer)]):
    """
    Retrieve the current user based on the provided JWT token.

    Args:
        token (Annotated[str, Depends(oauth_bearer)]): The JWT token used for authentication.

    Returns:
        AdminFront: The authenticated user object.

    Raises:
        Errors.CREDENTIALS_EXCEPTION: If the token is invalid, the username is not found in the token,
                                      or the user does not exist in the database.
    """
    try:
        payload = jwt.decode(token, SECURITY_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise Errors.CREDENTIALS_EXCEPTION
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise Errors.CREDENTIALS_EXCEPTION
    user = await AdminFront.find_one(AdminFront.username == token_data.username)
    if user is None:
        raise Errors.CREDENTIALS_EXCEPTION
    return user


async def get_current_active_user(
    current_user: Annotated[AdminFront, Depends(get_current_user)],
):
    """
    Retrieve the current active user.

    Args:
        current_user (Annotated[AdminFront, Depends(get_current_user)]): The current authenticated user.

    Returns:
        AdminFront: The current active user object.

    Raises:
        Errors.INACTIVE_USER_EXCEPTION: If the user is inactive.
    """
    if current_user.disabled:
        raise Errors.INACTIVE_USER_EXCEPTION
    return current_user
