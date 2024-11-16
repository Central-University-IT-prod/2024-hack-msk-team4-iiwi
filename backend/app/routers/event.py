from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from app.data import schemas
from app.data.models import Event, User, Category, Debter
from beanie.operators import In
from app.utils.security import get_current_active_user
from app.logger import logger
from app.data.errors import Errors
import uuid

router = APIRouter(prefix="/event", tags=["Event"])

@router.post("/post")
async def create_event(_: Annotated[schemas.User, Depends(get_current_active_user)], request: schemas.RequestEvent) -> schemas.ResponseEvent:
    categories = []
    user = await User.find_one(User.id == uuid.UUID(request.user_id), fetch_links=True)
    print(user)
    for categorie_name in request.category:
        category_instance = Category(
            name=categorie_name
        )
        print(category_instance, "\n")
        category_instance = await category_instance.create()
        categories.append(category_instance)
        
    event = Event(
        name=request.name,
        description=request.description,
        categories=categories,
        users=[user]
    )
    event_source = await event.create()
    user.event.append(event)
    await user.save()
    
    debter = Debter(
        debters=[],
        members=[],
        lender=user,
        debt=0
    )
    debter = await debter.create()
    return schemas.ResponseEvent(
        id=str(event_source.id),
        name=request.name,
        description=request.description,
        users=[schemas.MinUser(name=user.name, user_id=str(user.id))],
        categories=[schemas.MinCategorie(name=categorie.name, category_id=str(categorie.id)) for categorie in categories]
    )

@router.post("/add_user")
async def add_user(_: Annotated[schemas.User, Depends(get_current_active_user)], request: schemas.RequestAddUser) -> schemas.ResponseAddUser:
    event = await Event.find_one(Event.id == uuid.UUID(request.event_id))
    if not event:
        logger.error(f"Event {request.event_id} not found")
        raise Errors.EVENT_NOT_FOUND_EXCEPTION
    if not request.names:
        logger.error(f"Names {request} not found")
        raise Errors.USER_NOT_FOUND_EXCEPTION
    
    for k, username in enumerate(request.names):
        user = await User.find_one(User.phone == request.phones[k])
        if not user:
            logger.debug(f"User not found")
            user = User(
                name=username,
                phone=request.phones[k] if request.phones[k] else None
            )
            await user.create()
        event.users.append(user)
        user.event.append(event)
        await user.save()
    await event.save()
    
    return schemas.ResponseAddUser(
        result=True
    )

@router.get("/get")
async def get_event(_: Annotated[schemas.User, Depends(get_current_active_user)], request: schemas.RequestGetEvent = Depends()) -> schemas.ResponseEvent:
    event = await Event.find_one(Event.id == uuid.UUID(request.event_id), fetch_links=True)
    
    if not event:
        logger.error(f"Event not found")
        raise Errors.EVENT_NOT_FOUND_EXCEPTION
        
    return schemas.ResponseEvent(
        id=str(event.id),
        name=event.name,
        description=event.description,
        categories=[schemas.MinCategorie(name=category.name, category_id=str(category.id)) for category in event.categories],
        users=[schemas.MinUser(name=user.name, user_id=str(user.id)) for user in event.users]
    )
    
    
@router.get("/get_all")
async def get_all_events(_: Annotated[schemas.User, Depends(get_current_active_user)], request: schemas.RequestAllEvents = Depends()) -> list[schemas.ResponseAllEvents]:
    user = await User.find_one(User.id == uuid.UUID(request.user_id), fetch_links=True)
    
    if not user.event:
        logger.debug(f"Events not found")
        return []

    return [schemas.ResponseAllEvents(
        order_id=str(event.id),
        name=event.name,
        description=event.description,
    ) for event in user.event]