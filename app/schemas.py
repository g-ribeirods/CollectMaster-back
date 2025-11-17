from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr 
    password: str

class UserInDB(BaseModel):
    id: int
    name: str
    email: EmailStr
    hashed_password: str  


class UserPublic(BaseModel):
    id: int
    name: str
    email: EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class CollectionBase(BaseModel):
    name: str
    is_public: bool = True
    owner_id: int

class CollectionCreate(BaseModel):
    name: str
    is_public: bool = True
    owner_id: int

class CollectionInDB(CollectionBase):
    id: int
    image_url: Optional[str] = None # Campo para a foto
    value: float = 0.0  # Campo para o valor total da coleção
    itemCount: int = 0  # Campo para a contagem de itens

class CollectionPublic(BaseModel):
    id: int
    name: str
    is_public: bool
    owner_id: int
    image_url: Optional[str] = None
    value: float = 0.0
    itemCount: int = 0

    class Config:
        from_attributes = True