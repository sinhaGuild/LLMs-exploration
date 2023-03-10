from dotenv import load_dotenv
from fastapi import FastAPI
from app.config import swagger_parameters as swp
from app.routes import agent_router, base_router, chain_router, chat_router, sql_router

load_dotenv(override=True)  # load environment variables from .env.

app = FastAPI(
    title="Large Language Model Chaining (LLMC)",
    version="2.0.2",
    docs_url="/",
    swagger_ui_parameters=swp.ui_parameters,
    description=swp.description,
    contact=swp.contact,
    license_info=swp.license_info,
    openapi_tags=swp.tags_metadata,
)

# /base ROUTE
app.include_router(
    base_router.router,
    prefix="/base",
    tags=['🏠 Base'],
    responses={404: {"description": "Not found!"}, 418: {"description": "I'm a SQL!"}}
)


# /sql ROUTE
app.include_router(
    sql_router.router,
    prefix="/db",
    tags=['LLMs 🔗 Database'],
    responses={404: {"description": "Not found!"}, 418: {"description": "I'm a SQL!"}}
)


# /agent ROUTE
app.include_router(
    agent_router.router,
    prefix="/agent",
    tags=['Agents 🧠'],
    responses={404: {"description": "Not found!"}, 418: {"description": "I'm a Agent!"}}
)


# /chain ROUTE
app.include_router(
    chain_router.router,
    prefix="/chain",
    tags=['Cha ⫘⫘⫘⫘⫘ ins'],
    responses={404: {"description": "Not found!"}, 418: {"description": "I'm a Agent!"}}
)


# /chat ROUTE
app.include_router(
    chat_router.router,
    prefix="/chat",
    tags=['Chat 🤖'],
    responses={404: {"description": "Not found!"}, 418: {"description": "I'm a Agent!"}}
)