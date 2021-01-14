from fastapi import FastAPI, Response, status
from typing import Optional
from server.models import *
import bcrypt
import jwt
import datetime


app = FastAPI()


@app.post('/api/v1/user/register')
async def register_user(user: User,response: Response):
    userfound = usersCol.find_one({"email":user.email})
    if userfound:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message":"A user with this email already exists"}
    else:
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'),bcrypt.gensalt(10))
        user.password = hashed_password
        usersCol.insert_one(user.dict(by_alias=True))
        return user

#verifys if user login is valid
@app.post('/api/v1/user/login')
async def login_user(login: Login, response: Response):
    user = usersCol.find_one({"email": login.email})

    if bcrypt.checkpw(login.password.encode('utf-8'),user['password']):
        encoded_jwt = jwt.encode({
            "name": user['name'],
            "email": user['email']
        },"your-secret envvar",algorithm="HS256")
        return encoded_jwt
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message":"Wrong Email Or Password"}

# Decodes And Verifys the jwt token
@app.post('/api/v1/user/jwt/decode')
async def verifyjwt(jwtt: Jwt, response: Response):
    token = jwtt.token
    try:
        payload = jwt.decode(str(token),'your-secret envvar',algorithms=["HS256"])
        return payload
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Message":"Token invalid or expired"}





