from beanie import init_beanie, Document, UnionDoc
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app import MONGO_DSN, projectConfig
from app.routers import auth_sms, category, event, invite_link, debter, token, status
from app.routers import pay_debt

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

@asynccontextmanager
async def lifespan(_):
    client = AsyncIOMotorClient(MONGO_DSN, uuidRepresentation='standard')

    await init_beanie(
        database=client.get_default_database(),
        document_models=Document.__subclasses__() + UnionDoc.__subclasses__(),
    )
    yield
    client.close()

app = FastAPI(
    lifespan=lifespan,
    redoc_url=None,
    docs_url="/api/docs",
    title=projectConfig.__projname__,
    version=projectConfig.__version__,
    description=projectConfig.__description__,
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