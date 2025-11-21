from pydantic import BaseModel, EmailStr
from typing import Optional

# --- Schemas de Usuário (Mantenha estes) ---
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

# --- NOVOS Schemas de Coleção ---
class CollectionCreate(BaseModel):
    name: str
    is_public: bool = True
    owner_id: int

class CollectionInDB(BaseModel):
    id: int
    name: str
    is_public: bool
    owner_id: int
    image_url: Optional[str] = None
    value: float = 0.0
    itemCount: int = 0

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

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    quantity: int = 1
    estimated_value: float = 0.0
    collection_id: int

class ItemCreate(ItemBase):
    pass

class ItemInDB(ItemBase):
    id: int
    image_url: Optional[str] = None

class ItemPublic(ItemBase):
    id: int
    name: str
    description: Optional[str] = None
    quantity: int
    estimated_value: float
    collection_id: int
    image_url: Optional[str] = None

    class Config:
        from_attributes = True