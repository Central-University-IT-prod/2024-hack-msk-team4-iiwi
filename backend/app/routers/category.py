from fastapi import APIRouter, Depends
from typing import Annotated, List
from app.data import schemas
from app.data.models import Event, Category
from app.utils.security import get_current_active_user
from app.logger import logger
from app.data.errors import Errors
import uuid

router = APIRouter(prefix="/category", tags=["Category"])

@router.get("/get_id/{id}")
async def get_categor_by_id(_: Annotated[schemas.User, Depends(get_current_active_user)], id: str) -> schemas.Category:
    category = await Category.find_one(Category.id == uuid.UUID(id))

    return Category(
        name=category.name,
        description=category.description,
        debters=category.debters,
        lenders=category.lenders,
    )

@router.get("/get_all")
async def get_all_category(_: Annotated[schemas.User, Depends(get_current_active_user)], request: schemas.RequestCategory) -> list[schemas.RequestCategory]:
    events = await Event.find(Event.id == request.id_event).to_list()
    
    if not events:
        logger.error(f"Category not found")
        raise Errors.CATEGORY_NOT_FOUND_EXCEPTION
        
    return [schemas.ResponseCategory(
        name=event.name,
        category_id=event.categories
    )
      for event in events      
    ]

