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
class CollectionBase(BaseModel):
    name: str
    description: Optional[str] = None # Novo campo
    is_public: bool = True
    owner_id: int
    image_url: Optional[str] = None   # Agora faz parte da base

class CollectionCreate(CollectionBase):
    pass # Herda tudo de cima

class CollectionUpdate(BaseModel): # Novo Schema para Edição
    name: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None
    image_url: Optional[str] = None

class CollectionInDB(CollectionBase):
    id: int
    value: float = 0.0
    itemCount: int = 0

class CollectionPublic(CollectionInDB):
    class Config:
        from_attributes = True

# --- NOVOS Schemas de ITENS ---


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

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = None
    estimated_value: Optional[float] = None
    image_url: Optional[str] = None