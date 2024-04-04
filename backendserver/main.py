from typing import Annotated

from fastapi import Depends, FastAPI, Response, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer

# -------import auth module----------
import modules.auth_user.auth as auth_user
import modules.auth_user.depends as depends 
# -----------------------------------
from typing import List

# -------import user model-----------
from modules.user_model.usermodel import User
# -----------------------------------
from pymongo import MongoClient
import os

from dotenv import dotenv_values

config = dotenv_values(".env")


app = FastAPI(
    title="test webapp",
    version="0.2.0"

)

USERS_DATA = [
    {"username": "admin", "password": "adminpass"}
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print(app.database)
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

@app.post("/login")
async def auth(response: Response, data: User):
    user = await auth_user.check_username(data.username, data.password)
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    print(type(user))
    access_token = await auth_user.create_jwt_token({"sub" : user.get("username")})
    response.set_cookie("access_token", access_token, httponly=True)

    return {"access_token": access_token}
    
@app.get("/protected_resource")
async def register(request: Request, user: User = Depends(depends.get_user_from_token)):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    return user

@app.get("/", response_model=List[User])
async def monget(request: Request):
    users = list(request.app.database["users"].find())
    return users