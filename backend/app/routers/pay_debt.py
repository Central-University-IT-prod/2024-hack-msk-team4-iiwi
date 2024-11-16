from fastapi import APIRouter, HTTPException, Depends
from app.data import schemas
from typing import Annotated
from app.data.models import Category, Debter
from app.utils.security import get_current_active_user

router = APIRouter(prefix="/pay_dept", tags=["Pay dept"])

@router.post("/")
async def pay_dept(_: Annotated[schemas.User, Depends(get_current_active_user)], request: schemas.RequestPayDebt) -> schemas.ResponsePayDept:
    category = await Category.find_one(Category.id == request.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category nor found" )
    
    debter = await Debter.find_one(Debter.debters.id == request.user_id, fetch_links=True)
    if not debter:
        raise HTTPException(status_code=404, detail="Debt nor found" )
 
    if request.paid == debter.debt:
        await debter.debters.remove(request.user_id)
        await Category.debters.remove(request.user_id)
        return True
    else:
        debt = (debter.deb) - (request.paid)
        debter.debt = debt
        await debter.save()
        
        return schemas.ResponsePayDept(
            category_id=request.category_id,
            user_id=request.user_id,
            debt=debt
        )
