from typing import Annotated, List

from fastapi import Depends, FastAPI, Response, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer

# -------import auth module----------
import modules.auth_user.auth as auth_user
import modules.auth_user.depends as depends 
# -----------------------------------

# -------import user model-----------
from modules.user_model.usermodel import User
# -----------------------------------


# ------------import enviroment-----------------------
from dotenv import dotenv_values
config = dotenv_values(".env")
# ----------------------------------------------------


# -------------create fastapi app---------------------
app = FastAPI(
    title="test webapp",
    version="0.2.0"

)
from modules.database.database import router_database
app.include_router(router_database)
# ----------------------------------------------------

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# -----------------connect to mongodb-----------------
from pymongo import MongoClient

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["URL"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print(app.database)
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
# ----------------------------------------------------


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
