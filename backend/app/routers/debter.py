from fastapi import APIRouter, Depends
from typing import Annotated
from beanie.operators import In
from app.data import schemas
from app.data.models import Category, Event, Debter, User
from app.logger import logger
from app.data.errors import Errors
import uuid
from app.utils.security import get_current_active_user

router = APIRouter(prefix="/debter", tags=["Debter"])


@router.post("/create")
async def create_depter(_: Annotated[schemas.User, Depends(get_current_active_user)], request: list[schemas.RequestCreateDebter]) -> schemas.RequestCreateDebter:
    debters_count = 0
    depters_paid = []
    debters = []
    sch_debteres = []
    paid = 0
    members = []

    for user in request:
        if user.auto:
            debters_count = 0
            depters_paid = []
            debters = []
            sch_debteres = []
            paid = 0
            members = []
        else:
            category = await Category.find_one(Category.id == user.category_id)
            if user.debter:
                depters_paid.append(user.paid)
                debters_count += 1
                find_debter = await User.find_one(User.id == user.user_id)
                debters.append(find_debter)
                sch_debteres.append(schemas.User(
                    id=str(find_debter.id),
                    name=find_debter.name,
                    category=schemas.Category(
                        name=find_debter.category.name,
                        description=find_debter.category.description,
                        debters=find_debter.category.debters,
                        lenders=find_debter.category.lenders,
                        lenders_amount=find_debter.category.lenders_amount
                    ),
                    event=str(find_debter.event.id),
                ))
            else:
                paid = user.paid
                find_lender = await User.find_one(User.id == user.user_id)
                
                debt = paid / debters_count
                
                for member in user.members:
                    members.append({"user_id": member.user_id, "name": member.name, "debt": member.debt})
        
        new = Debter(
            debter=debters,
            lender=find_lender,
            debt=paid,
            members=members
        )
        
        await new.create()
        category = await Category.find_one(Category.id == user.category_id)
        if user.debter:
            depters_paid.append(user.paid)
            debters_count += 1
            find_debter = await User.find_one(User.id == user.user_id, fetch_links=True)
            debters.append(find_debter)
            sch_debteres.append(schemas.User(
                id=str(find_debter.id),
                name=find_debter.name,
                category=schemas.Category(
                    name=find_debter.category.name,
                    description=find_debter.category.description,
                    debters=find_debter.category.debters,
                    lenders=find_debter.category.lenders,
                    lenders_amount=find_debter.category.lenders_amount
                ),
                event=str(find_debter.event.id),
            ))
        else:
            paid = user.paid
            find_lender = await User.find_one(User.id == user.user_id)
            
            
    debt = paid / debters_count
    
    for debter in debters:
        members.append({"user_id": debter.id, "name": debter.name, "debt": debt, "status": 0})
    
    new = Debter(
        category=category,
        debters=debters,
        lender=find_lender,
        debt=paid,
        already_paid=depters_paid,
        members=members
    )
    
    await new.create()
            
    return schemas.ResponseCreateDebter(
        debters=sch_debteres,
        lender=new.lender,
        debt=new.debt,
        members=new.members       
    )

        
        
@router.get("/get_all")
async def get_all_debters_in_event(_: Annotated[schemas.User, Depends(get_current_active_user)], request: schemas.RequestGetEvent = Depends()) -> list[schemas.ResponseGetDebt]:
    event = await Event.find_one(Event.id == uuid.UUID(request.event_id), fetch_links=True)
    
    if not event:
        logger.error("Event not found")
        raise Errors.EVENT_NOT_FOUND_EXCEPTION
    
    users = [user.id for user in event.users]
    
    if not users:
        logger.error("Users not found")
        raise Errors.USER_NOT_FOUND_EXCEPTION
    
    debters = await Debter.find(In(Debter.lender.id, users), fetch_links=True).to_list()
    
    return [schemas.ResponseGetDebt(
        debters=[schemas.MinUser(name=debter.name, user_id=str(debter.id)) for debter in debter.debters],
        lender=schemas.MinUser(name=debter.lender.name, user_id=str(debter.lender.id)),
        dept=debter.debt,
        members=debter.members
    ) for debter in debters]