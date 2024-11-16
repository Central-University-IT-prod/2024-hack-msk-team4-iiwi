from pydantic import BaseModel, Field
from typing import Optional, List
from app.data.models import User, Category, MoneyStatus


class Category(BaseModel):
    name: str = Field(..., description="Name of the category", example="Groceries")
    description: Optional[str] = Field(None, description="Description of the category", example="Monthly grocery expenses")
    debters: list[User] = Field(..., description="List of users who owe money", example=[])
    lenders: list[User] = Field(..., description="List of users who lent money", example=[])

class Event(BaseModel):
    name: str = Field(..., description="Name of the event", example="Birthday Party")
    description: str = Field(..., description="Description of the event", example="John's 30th birthday celebration")
    users: List[User] = Field(..., description="List of users participating in the event", example=[])
    compleated: bool = Field(..., description="Indicates if the event is completed", example=False)
    categories: List[Category] = Field(..., description="List of categories in the event", example=[])

class User(BaseModel):
    id: str = Field(..., description="Unique identifier for the user", example="user_123")
    name: str = Field(..., description="Name of the user", example="John Doe")
    category: Category = Field(..., description="Category associated with the user")
    event: Event = Field(..., description="Event associated with the user")

class ResponsePayDept(BaseModel):
    category_id: str = Field(..., description="Unique identifier for the category", example="cat_123")
    user_id: str = Field(..., description="Unique identifier for the user", example="user_123")
    debt: int = Field(..., description="Amount of debt", example=100)
    
class RequestSetStatus(BaseModel):
    debter_id: str = Field(..., description="Unique identifier for the debtor", example="user_123")
    status: MoneyStatus = Field(..., description="Status of the money", example=MoneyStatus.MONEY_SENT)
    
class ResponseSetStatus(BaseModel):
    debter_id: str = Field(..., description="Unique identifier for the debtor", example="user_123")
    status: MoneyStatus = Field(..., description="Status of the money", example=MoneyStatus.MONEY_SENT)

class RequestGetStatus(BaseModel):
    debter_id: str = Field(..., description="Unique identifier for the debtor", example="user_123")
    
class ResponseGetStatus(BaseModel):
    debter_id: str = Field(..., description="Unique identifier for the debtor", example="user_123")
    status: MoneyStatus = Field(..., description="Status of the money", example=MoneyStatus.MONEY_SENT)

class RequestPayDebt(BaseModel):
    category_id: str = Field(..., description="Unique identifier for the category", example="cat_123")
    user_id: str = Field(..., description="Unique identifier for the user", example="user_123")
    MONEY_SENT: int = Field(..., description="Amount MONEY_SENT", example=50)
    
class RequestInviteLink(BaseModel):
    event_id: str = Field(..., description="Unique identifier for the event", example="event_123")
    name: str = Field(..., description="Name of the invitee", example="Jane Doe")

class ResponseInviteLink(BaseModel):
    link: str = Field(..., description="Generated invite link", example="http://example.com/invite?token=abc123")
    
class RequestCheckLink(BaseModel):
    short_link: str = Field(
        ...,
        description="Link which user logs in with",
        example="http://example.com/invite?token=abc123"
    )
    
class ResponseCheckLink(BaseModel):
    user: User = Field(
        ...,
        description="User who clicked on the link"
    )
    
class RequestCheckCode(BaseModel):
    code: int = Field(
        ...,
        description="Code sent to user's phone number",
        example=123456
    )
    phone: str = Field(
        ...,
        description="Phone number to which the code is sent",
        example="+1234567890"
    )
    
class ResponseCheckCode(BaseModel):
    status: bool = Field(
        ...,
        description="Shows if the code was checked or not",
        example=True
    )
    user_id: str = Field(
        ...,
        description="User's unique id",
        example="user_123"
    )
    
class RequestSendCode(BaseModel):
    phone: str = Field(
        ...,
        description="Phone number to which the code is sent",
        example="+1234567890"
    )
    again: bool = Field(
        ...,
        description="Indicates whether the code has been sent again",
        example=False
    )
    
class ResponseSendCode(BaseModel):
    status: bool = Field(
        ...,
        description="Shows if the code has been sent or not",
        example=True
    )

class RequestEvent(BaseModel):
    user_id: str = Field(
        ...,
        description="User's unique id",
        example="user_123"
    )
    name: str = Field(
        ...,
        description="Event name",
        example="Birthday Party"
    )
    description: str = Field(
        ...,
        description="Event description",
        example="John's 30th birthday celebration"
    )
    category: List[str] = Field(
        ...,
        description="Categories in the event",
        example=["cat_123", "cat_456"]
    )
    
class RequestUser(BaseModel):
    name: str = Field(
        ...,
        description="Username",
        example="John Doe"
    )
    number: int = Field(
        ...,
        description="User's phone number",
        example=1234567890
    )
    categories: Optional[List[str]] = Field(
        None,
        description="Category ids",
        example=["cat_123", "cat_456"]
    )
    event: int = Field(
        ...,
        description="User's event Id",
        example=1
    )
    
class ResponseUser(BaseModel):
    name: str = Field(
        ...,
        description="Username",
        example="John Doe"
    )
    number: int = Field(
        ...,
        description="User's phone number",
        example=1234567890
    )
    category: Optional[List[str]] = Field(
        None,
        description="Category ids",
        example=["cat_123", "cat_456"]
    )
    event: int = Field(
        ...,
        description="User's event Id",
        example=1
    )

class RequestAddUser(BaseModel):
    event_id: str = Field(..., description="Unique identifier for the event", example="event_123")
    names: List[str] = Field(..., description="List of names of users to be added", example=["Jane Doe", "John Smith"])
    phones: List[Optional[str]] = Field(..., description="List of phone numbers of users to be added", example=["+1234567890", "+0987654321"])
    
class ResponseAddUser(BaseModel):
    result: bool = Field(..., description="Result of the add user operation", example=True)

class RequestCategory(BaseModel):
    id_event: str = Field(
        ...,
        description="Event id",
        example="event_123"
    )

class ResponseCategory(BaseModel):
    name: str = Field(
        ...,
        description="Category name",
        example="Groceries"
    )
    category_id: str = Field(
        ...,
        description="Unique category id",
        example="cat_123"
    )
    
class UserDebt(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user", example="user_123")
    name: str = Field(..., description="Name of the user", example="John Doe")
    debt: int = Field(..., description="Amount of debt", example=100)
    status: MoneyStatus = Field(
        default=MoneyStatus.INITIAL,
        description="Status of the money",
        example=MoneyStatus.MONEY_SENT
    )

class RequestCreateDebter(BaseModel):
    category_id: str = Field(
        ...,
        description="Category id",
        example="cat_123"
    )
    user_id: str = Field(
        ...,
        description="Id of the category for which there is a debt",
        example="user_123"
    )
    debter: bool = Field(
        ...,
        description="Whether a person is a debtor",
        example=True
    )
    auto: bool = Field(
        True,
        description="Determines how the payment will be divided: in half or in different amounts",
        example=True
    )
    members: list[UserDebt] = Field(
        [],
        description="List of users who have debt",
        example=[]
    )
    
class MinCategorie(BaseModel):
    name: str = Field(..., description="Name of the category", example="Groceries")
    category_id: str = Field(..., description="Unique identifier for the category", example="cat_123")

class MinUser(BaseModel):
    name: Optional[str] = Field(None, description="Name of the user", example="John Doe")
    user_id: str = Field(..., description="Unique identifier for the user", example="user_123")

class ResponseEvent(BaseModel):
    id: str = Field(
        ...,
        description="Event's unique id",
        example="event_123"
    )
    name: str = Field(
        ...,
        description="Event name",
        example="Birthday Party"
    )
    description: str = Field(
        ...,
        description="Event description",
        example="John's 30th birthday celebration"
    )
    categories: list[MinCategorie] = Field(
        ...,
        description="Categories in event",
        example=[]
    )
    users: List[MinUser] = Field(
        ...,
        description="Users in event",
        example=[]
    )
    
    
class RequestAllEvents(BaseModel):
    user_id: str = Field(
        ...,
        description="User's unique id",
        example="user_123"
    )
    
    
class ResponseAllEvents(BaseModel):
    name: str  = Field(
        ...,
        description="Name of event",
        example="Birthday Party"
    )
    description: str = Field(
        ...,
        description="Event description",
        example="John's 30th birthday celebration"
    )
    order_id: str = Field(
        ...,
        description="Order id",
        example="order_123"
    )
    
    
class RequestGetEvent(BaseModel):
    event_id: str = Field(
        ...,
        description="Unique identifier for the event",
        example="event_123"
    )
    
class ResponseGetDebt(BaseModel):
    debters: List[MinUser] = Field(..., description="List of debtors", example=[])
    lender: MinUser = Field(..., description="Lender", example=MinUser(user_id="user_456"))
    dept: float = Field(..., description="Amount of debt", example=100.0)
    members: Optional[list[UserDebt]] = Field(None, description="List of users who have debt", example=[])

class ResponseBearerToken(BaseModel):
    """
    ResponseBearerToken model representing the response of the bearer token.
    """

    access_token: str = Field(
        ...,
        description="Access token for the user.",
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    )
    token_type: str = Field(..., description="Type of the token.", example="Bearer")


class ResponseCreateDebter(BaseModel):
    debter: User = Field(
        ...,
        description="User who owes money to another user"
    )
    lender: User = Field(
        ...,
        description="User to whom the other user owes money"
    )
    debt: float = Field(
        ...,
        description="Amount of debt",
        example=100.0
    )
    members: list[UserDebt] = Field(
        ...,
        description="List of users who have debt",
        example=[]
    )
    