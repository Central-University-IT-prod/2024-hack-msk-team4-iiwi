import sys
import os

from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from beanie import init_beanie, Document, UnionDoc
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import pytest
import mongomock


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
from routers import auth_sms, category, event, invite_link, debter, token, status, pay_debt

@asynccontextmanager
async def lifespan(_):
    client = AsyncIOMotorClient("mongodb://mongodb://localhost:27017/iiwi", uuidRepresentation='standard')

    await init_beanie(
        database=client.get_default_database(),
        document_models=Document.__subclasses__() + UnionDoc.__subclasses__(),
    )
    yield
    client.close()
    


def start_application():
    tags_metadata = [
    {
        "name": "Sms Code",
        "description": "Operations with sms code.",
    },
    {
        "name": "Category",
        "description": "Operations with categories **with debters and lenders.**",
    },
    {
        "name": "Event",
        "description": "Operations with Events.",
    },
    {
        "name": "Invite Link",
        "description": "Operations with Invite Links. **Generate and check.**",
    },
    {
        "name": "Token",
        "description": "Operations with Bearer. For **frontend.**",
    },
    {
        "name": "Status",
        "description": "Operations with status.",
    },
    {
        "name": "Pay dept",
        "description": "Operations with dept. **Pay dept.**",
    },
    {
        "name": "Debter",
        "description": "Operations with debters. **Get all debters in event.**",
    },
    
]
    app = FastAPI(
    lifespan=lifespan,
    redoc_url=None,
    docs_url="/api/docs",
    openapi_tags=tags_metadata,
)

    app.include_router(auth_sms.router)
    app.include_router(category.router)
    app.include_router(event.router)
    app.include_router(invite_link.router)
    app.include_router(debter.router)
    app.include_router(token.router)
    app.include_router(status.router)
    app.include_router(pay_debt.router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    _app = start_application()
    yield _app
