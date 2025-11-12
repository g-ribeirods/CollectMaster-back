import json
from typing import List, Optional
from .schemas import UserInDB

DB_FILE = "users.json"

def load_users() -> List[UserInDB]:
    """Carrega todos os usuários do arquivo JSON."""
    try:
        with open(DB_FILE, "r") as f:
            users_data = json.load(f)
            return [UserInDB(**user) for user in users_data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_users(users: List[UserInDB]):
    """Salva a lista completa de usuários no arquivo JSON."""
    with open(DB_FILE, "w") as f:
        users_data = [user.model_dump() for user in users]
        json.dump(users_data, f, indent=2)

def get_user_by_email(email: str) -> Optional[UserInDB]:
    """Busca um usuário pelo email."""
    users = load_users()
    for user in users:
        if user.email == email:
            return user
    return None

def create_user(user: UserInDB) -> UserInDB:
    """Adiciona um novo usuário ao arquivo JSON."""
    users = load_users()

    users.append(user)
    
    save_users(users)
    return user