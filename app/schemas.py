from pydantic import BaseModel, EmailStr

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