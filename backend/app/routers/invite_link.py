from fastapi import APIRouter, Depends
from typing import Annotated
from app.data import schemas
from app.data.models import InviteLink, Event, User
from app.utils.security import get_current_active_user
import random
import uuid
import string

router = APIRouter(prefix="/invite_link", tags=["Invite Link"])

@router.get("/generate")
async def generate_invite_link(_: Annotated[schemas.User, Depends(get_current_active_user)], event: schemas.RequestInviteLink) -> schemas.ResponseInviteLink:
    link = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    event = await Event.find_one(Event.id == uuid.UUID(event.event_id))
    
    inviteLink = InviteLink(
        link=link,
        short_link=link,
        name_user=event.name,
        event=event
    )
    await inviteLink.create()
    return schemas.ResponseInviteLink(
        link=inviteLink.link
    )

@router.get("/check/{short_link}")
async def check_invite_link(_: Annotated[schemas.User, Depends(get_current_active_user)], short_link: str) -> schemas.ResponseCheckLink:
    inviteLink = await InviteLink.find_one(InviteLink.short_link == short_link)
    user = await User.find_one(User.id == inviteLink)
    
    return schemas.ResponseCheckLink(
        user=schemas.User(
            id=user.id,
            name=user.name,
            category=user.category,
            event=user.event
        )
    )