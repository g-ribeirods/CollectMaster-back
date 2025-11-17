import json
from typing import List, Optional
from .schemas import UserInDB, CollectionInDB

DB_FILE = "users.json"

def load_users() -> List[UserInDB]:
    try:
        with open(DB_FILE, "r") as f:
            users_data = json.load(f)
            return [UserInDB(**user) for user in users_data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_users(users: List[UserInDB]):
    with open(DB_FILE, "w") as f:
        users_data = [user.model_dump() for user in users]
        json.dump(users_data, f, indent=2)

def get_user_by_email(email: str) -> Optional[UserInDB]:
    users = load_users()
    for user in users:
        if user.email == email:
            return user
    return None

def create_user(user: UserInDB) -> UserInDB:
    users = load_users()

    users.append(user)
    
    save_users(users)
    return user

COLLECTIONS_DB_FILE = "collections.json"

def load_collections() -> List[CollectionInDB]:
    try:
        with open(COLLECTIONS_DB_FILE, "r") as f:
            collections_data = json.load(f)
            return [CollectionInDB(**col) for col in collections_data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_collections(collections: List[CollectionInDB]):
    with open(COLLECTIONS_DB_FILE, "w") as f:
        collections_data = [col.model_dump() for col in collections]
        json.dump(collections_data, f, indent=2)

def create_collection_in_db(collection: CollectionInDB) -> CollectionInDB:
    collections = load_collections()
    collections.append(collection)
    save_collections(collections)
    return collection

def get_collections_by_owner_id(owner_id: int) -> List[CollectionInDB]:
    collections = load_collections()
    return [col for col in collections if col.owner_id == owner_id]