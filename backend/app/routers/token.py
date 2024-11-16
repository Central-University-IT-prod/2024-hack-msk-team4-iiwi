from datetime import timedelta
from typing import Annotated

from app import ACCESS_TOKEN_EXPIRE_MINUTES
from app.data.errors import Errors
from app.data.schemas import ResponseBearerToken
from app.utils.security import authenticate_user, create_access_token
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_versionizer.versionizer import api_version

router = APIRouter()

@router.post(
    "/token/new",
    tags=["Token"],
    responses={
        401: {
            "description": "Could not validate credentials. Please ensure that your username and password are correct and try again."
        },
        400: {
            "description": "Inactive user. Your account is currently inactive. Please contact support to reactivate your account."
        },
    },
)
@api_version(1)
async def login_get_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> ResponseBearerToken:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise Errors.UNAUTHORIZED_EXCEPTION
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user[0].username}, expires_delta=access_token_expires
    )
    return ResponseBearerToken(access_token=access_token, token_type="bearer")
