from fastapi import APIRouter, HTTPException
from typing import List, Optional
from .. import schemas, db_json

router = APIRouter()

# Retorna lista de usuários (com opção de busca simples)
@router.get("/", response_model=List[schemas.UserPublic])
async def read_users(search: Optional[str] = None):
    users = db_json.load_users()
    
    if search:
        search_lower = search.lower()
        # Filtra por nome ou email
        users = [
            u for u in users 
            if search_lower in u.name.lower() or search_lower in u.email.lower()
        ]
        
    return users

# Retorna um usuário específico pelo ID
@router.get("/{user_id}", response_model=schemas.UserPublic)
async def read_user(user_id: int):
    users = db_json.load_users()
    user = next((u for u in users if u.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user