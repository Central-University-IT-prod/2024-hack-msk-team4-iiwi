from beanie import Document, Link
from enum import IntEnum
from typing import Dict, List, Optional
from pydantic import Field, BaseModel
from uuid import UUID, uuid4
from app.data import schemas


class MoneyStatus(IntEnum):
    INITIAL = 0
    MONEY_SENT = 1
    MONEY_RESEIVED = 2
    
class Category(Document):
    id: UUID = Field(alias="_id", unique=True, default_factory=uuid4)
    name: str
    description: Optional[str] = Field(None)
    debters: Optional[list[int]] = Field([])
    lenders: Optional[list[Dict[str, float]]] = Field([])
    
class UserDebt(BaseModel):
    user_id: str
    name: str
    debt: int
    status: MoneyStatus = Field(
        default=MoneyStatus.INITIAL
    )
    
class User(Document):
    id: UUID = Field(alias="_id", unique=True, default_factory=uuid4)
    name: Optional[str] = Field(None)
    phone: Optional[str] = Field(None)
    category: Optional[Link["Category"]] = Field(None)
    event: List[Link["Event"]] = Field([])

#TODO: Fix UUID duplicating
class Event(Document):
    id: UUID = Field(alias="_id", unique=True, default_factory=uuid4)
    name: str
    description: str
    users: List[Link["User"]]
    compleated: bool = Field(default=False)
    categories: List[Link["Category"]]

class InviteLink(Document):
    id: UUID = Field(alias="_id", unique=True, default_factory=uuid4)
    link: str
    short_link: str
    event: Link["Event"]
    name_user: str
    
class Debter(Document):
    id: UUID = Field(alias="_id", unique=True, default_factory=uuid4)
    debters: list[Link["User"]]
    members: list[UserDebt]
    lender: Link["User"]
    debt: float
    lender_wallet: Optional[str] = Field(default=None)
    wallet: bool = Field(default=False)

class AuthCode(Document):
    id: UUID = Field(alias="_id", unique=True, default_factory=uuid4)
    code: int
    phone: str
    
class SecretAdmin(Document):
    """
    SecretAdmin model representing an admin user with additional security attributes.

    Attributes:
        hashed_password (str): Hashed password for the admin user.
    """

    hashed_password: str


class AdminFront(Document):
    """
    AdminFront model representing an admin user for the frontend.

    Attributes:
        username (str): Unique username of the admin.
        disabled (bool): Indicates if the admin account is disabled. Default is False.
        full_name (str): Full name of the admin. Default is None.
        secret (Link[SecretAdmin]): Link to the SecretAdmin document containing security details.
    """

    username: str = Field(unique=True)
    disabled: bool = Field(default=False)
    full_name: str = Field(default=None)
    secret: Link[SecretAdmin] = Field()


class Token(BaseModel):
    """
    Token model representing an access token.

    Attributes:
        access_token (str): The access token string.
        token_type (str): The type of the token, typically "bearer".
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    TokenData model representing the data contained in a token.

    Attributes:
        username (str): The username associated with the token.
    """

    username: str
