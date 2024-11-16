from fastapi import APIRouter, Depends
from typing import Annotated
from app.data import schemas
from app.data.errors import Errors
from app.data.models import AuthCode, User
import random
import requests
import asyncio
from app import MTS_API_LOGIN, MTS_API_PASSWORD, MTS_API_URL
from app.utils.security import get_current_active_user

router = APIRouter(prefix="/code", tags=["Sms Code"])

@router.post("/send")
async def send_code(_: Annotated[schemas.User, Depends(get_current_active_user)], request: schemas.RequestSendCode) -> schemas.ResponseSendCode:
    code = random.randint(1000, 9999)
    response = await asyncio.to_thread(requests.get(
        url=MTS_API_URL,
        params={
            'login': MTS_API_LOGIN,
            'password': MTS_API_PASSWORD,
            'msisdn': request.phone,
            'from': f'iiwi',
            'message': f'Ваш код подтверждения: {code}'
        }
    ))
    if request.again:
        code_instance = await AuthCode.find_one(AuthCode.phone == request.phone)
        code_instance.code = code
        await code_instance.save()
    else:
        code_instance = AuthCode(
            code=code,
            phone=request.phone
        )
        await code_instance.create()
        
@router.post("/check")
async def check_code(_: Annotated[schemas.User, Depends(get_current_active_user)], request: schemas.RequestCheckCode) -> schemas.ResponseCheckCode:
    code_instance = await AuthCode.find_one(AuthCode.phone == request.phone)
    if code_instance.code == request.code:
        return schemas.ResponseCheckCode(
            status=True
        )
    else:
        return schemas.ResponseCheckCode(
            status=False
        )

@router.post("/test/check")
async def check_code_test(_: Annotated[schemas.User, Depends(get_current_active_user)], request: schemas.RequestCheckCode) -> schemas.ResponseCheckCode:
    code_instance = await AuthCode.find_one(AuthCode.phone == request.phone)
    user = await User.find_one(User.phone == request.phone)
    if user is None:
        user = User(
            phone=request.phone
        )
        await user.create()
    if code_instance.code == request.code:
        return schemas.ResponseCheckCode(
            status=True,
            user_id=str(user.id)
        )
    else:
        raise Errors.CODE_INVALID