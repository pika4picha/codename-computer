import jwt
from fastapi import HTTPException, status, Request,Depends
from datetime import datetime, timedelta 
import main 
# --------------get alg and sk for jwt------------
import os
from dotenv import load_dotenv


ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.environ.get("SECRET_KEY")
# ------------------------------------------------

async def get_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    return token

async def get_user_from_token(token: str = Depends(get_token)):
    
    try:
        payload = jwt.decode(jwt = token, key = SECRET_KEY, algorithms = ALGORITHM)
    except jwt.PyJWTError:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)

    expire: str = payload.get("exp")
    
    if (int(expire) <= datetime.utcnow().timestamp()) or (not expire):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    
    username: str = payload.get("sub")
    if not username:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    
    for user in main.USERS_DATA:
        if username == user.get("username"):
            return {"username": username}
    
    raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    



