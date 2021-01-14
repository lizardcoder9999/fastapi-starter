import os
from pydantic import BaseModel, fields
from bson import ObjectId
import pymongo


client = pymongo.MongoClient('your mongo uri var')
db = client['fastapi']
usersCol = db['users']


class User(BaseModel):
    _id: ObjectId
    name: str
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str

class Jwt(BaseModel):
    token: str


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
