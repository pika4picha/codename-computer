from fastapi import APIRouter, Request
from typing import Annotated, List
from modules.user_model.usermodel import User


router_database = APIRouter()


@router_database.get("/users", response_model=List[User])
async def monget(request: Request):
    users = list(request.app.database["users"].find())
    # for user in users:
    #     user['_id'] = str(user['_id'])
    return users