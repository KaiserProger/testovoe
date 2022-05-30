from fastapi import FastAPI
import sys
from domain.config.read import ConfigReader

from domain.db.db import Db
from domain.deps.deps import dummy, get_service_collection
from domain.usecases.account_crud import CrudAccount
from endpoints.account import account_router
from endpoints.auth import auth_router

sys.path.append("./domain")
sys.path.append("./endpoints")
db_class = Db("postgresql+asyncpg://postgres:postgres@db/maindb")
temp_crud: CrudAccount = get_service_collection().\
    crud_cache[CrudAccount]
config = ConfigReader()

app = FastAPI()


@app.on_event("startup")
async def init() -> None:
    await db_class.init_tables()
    await db_class.init_app_values(config.model.temp_acc_id)


@app.on_event("shutdown")
async def shut() -> None:
    await db_class.engine.dispose()

app.dependency_overrides[dummy] = db_class.create_session
app.include_router(account_router)
app.include_router(auth_router)
