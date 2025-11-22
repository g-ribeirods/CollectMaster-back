import json
from typing import List, Optional
from .schemas import UserInDB, CollectionInDB, ItemInDB, ItemUpdate, CollectionUpdate

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
            data = json.load(f)
            return [CollectionInDB(**col) for col in data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_collections(collections: List[CollectionInDB]):
    with open(COLLECTIONS_DB_FILE, "w") as f:
        # Converte para dicionário para salvar no JSON
        data = [col.model_dump() for col in collections]
        json.dump(data, f, indent=2)

def create_collection_in_db(collection: CollectionInDB) -> CollectionInDB:
    collections = load_collections()
    collections.append(collection)
    save_collections(collections)
    return collection

def get_collections_by_owner_id(owner_id: int) -> List[CollectionInDB]:
    collections = load_collections()
    return [col for col in collections if col.owner_id == owner_id]

def update_collection_in_db(collection_id: int, collection_update: CollectionUpdate) -> Optional[CollectionInDB]:
    collections = load_collections()
    
    for i, col in enumerate(collections):
        if col.id == collection_id:
            # Pydantic magic: atualiza apenas os campos enviados
            update_data = collection_update.model_dump(exclude_unset=True)
            updated_col = col.model_copy(update=update_data)
            
            collections[i] = updated_col
            save_collections(collections)
            return updated_col
            
    return None

ITEMS_DB_FILE = "items.json"

def load_items() -> List[ItemInDB]:
    try:
        with open(ITEMS_DB_FILE, "r") as f:
            data = json.load(f)
            return [ItemInDB(**item) for item in data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_items(items: List[ItemInDB]):
    with open(ITEMS_DB_FILE, "w") as f:
        data = [item.model_dump() for item in items]
        json.dump(data, f, indent=2)

def create_item_in_db(item: ItemInDB) -> ItemInDB:
    items = load_items()
    items.append(item)
    save_items(items)
    
    # Mágica: Atualiza o valor total e contagem na coleção pai!
    update_collection_stats(item.collection_id)
    
    return item

def get_items_by_collection_id(collection_id: int) -> List[ItemInDB]:
    items = load_items()
    return [i for i in items if i.collection_id == collection_id]

def update_collection_stats(collection_id: int):
    """Recalcula os totais da coleção e salva."""
    all_items = get_items_by_collection_id(collection_id)
    all_collections = load_collections()
    
    for col in all_collections:
        if col.id == collection_id:
            col.itemCount = sum(i.quantity for i in all_items)
            col.value = sum(i.estimated_value * i.quantity for i in all_items)
            break
    
    save_collections(all_collections)

def get_item_by_id(item_id: int) -> Optional[ItemInDB]:
    items = load_items()
    for item in items:
        if item.id == item_id:
            return item
    return None

def update_item_in_db(item_id: int, item_update: ItemUpdate) -> Optional[ItemInDB]:
    items = load_items()
    
    for i, item in enumerate(items):
        if item.id == item_id:
            # Atualiza apenas os campos que foram enviados (não nulos)
            update_data = item_update.model_dump(exclude_unset=True)
            updated_item = item.model_copy(update=update_data)
            
            items[i] = updated_item
            save_items(items)
            
            # Atualiza estatísticas da coleção
            update_collection_stats(updated_item.collection_id)
            return updated_item
            
    return None

def delete_item_in_db(item_id: int) -> bool:
    items = load_items()
    
    for i, item in enumerate(items):
        if item.id == item_id:
            collection_id = item.collection_id # Guarda o ID para atualizar estatísticas
            
            items.pop(i) # Remove da lista
            save_items(items)
            
            update_collection_stats(collection_id) # Recalcula
            return True
            
    return False