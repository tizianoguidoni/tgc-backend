from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    packs: int
    streak: int
    last_login: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class CardResponse(BaseModel):
    id: int
    name: str
    rarity: str
    image_url: str
    flavor: str = ""
    power: int = 0
    sigma: int = 0
    based: int = 0

    class Config:
        from_attributes = True

class UserCardResponse(BaseModel):
    card: CardResponse
    count: int

    class Config:
        from_attributes = True
