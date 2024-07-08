from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class UserCreate (BaseModel):
    email: EmailStr
    password: str

class UserOut (BaseModel):
    email: str
    password: str
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    user_id : int
    user : UserOut
    class Config:
        from_attributes = True


class PostVote(BaseModel):
    Post: Post
    votes: int
        # will tell pydantic  model to read  the data even fi it's not a dic
    class Config:
        from_attributes = True
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id:int
    dir: conint(le=1)