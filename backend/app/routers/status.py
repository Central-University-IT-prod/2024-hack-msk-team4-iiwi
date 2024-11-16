from fastapi import APIRouter, Depends
from typing import Annotated
from app.data import schemas
from app.data.models import InviteLink, Event, User, Debter
from app.utils.security import get_current_active_user
from app.data.errors import Errors
import random
import uuid
from app.logger import logger

router = APIRouter(prefix="/status", tags=["Status"])

@router.post("/set")
async def set_status(_: Annotated[schemas.User, Depends(get_current_active_user)], request: schemas.RequestSetStatus) -> schemas.ResponseSetStatus:
    debter = await Debter.find_one(Debter.id == uuid.UUID(request.debter_id))
    
    debter.status = request.status
    await debter.save()
    
    if not debter:
        logger.error(f"Debter not found")
        raise Errors.DEBTER_NOT_FOUND_EXCEPTION
        
    return schemas.ResponseSetStatus(
        status=request.status,
        debter_id=request.debter_id
    )

@router.get("/get")
async def get_status(_: Annotated[schemas.User, Depends(get_current_active_user)], request: schemas.RequestGetStatus = Depends()) -> schemas.ResponseGetStatus:
    debter = await Debter.find_one(Debter.id == uuid.UUID(request.debter_id))
    
    if not debter:
        logger.error(f"Debter not found")
        raise Errors.DEBTER_NOT_FOUND_EXCEPTION
        
    return schemas.ResponseGetStatus(
        status=debter.status,
        debter_id=request.debter_id
    )