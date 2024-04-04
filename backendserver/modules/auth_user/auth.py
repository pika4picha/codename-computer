import jwt
from datetime import datetime, timedelta 

# --------------get alg and sk for jwt------------
import os
from dotenv import load_dotenv
load_dotenv()

ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.environ.get("SECRET_KEY")
# ------------------------------------------------

async def create_jwt_token(data: dict):
    """
    Create jwt tocken for auth user, with expire time 10 minutes.
    """
    encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = 10)
    encode.update({"exp" : expire})
    user_jwt = jwt.encode(encode, key = SECRET_KEY, algorithm = ALGORITHM)
    return user_jwt

async def check_password(passwordlib: str, password: str) -> bool:
    return passwordlib == password

async def check_username(userdata, username: str, password):
    for user in userdata:
        print(user)
        if username == user.get("username") and await check_password(user.get("password"), password):
            return {"username": username}
    return None
 