from fastapi import APIRouter, HTTPException, status
from typing import List
from .. import schemas, db_json

router = APIRouter()

@router.post("/", response_model=schemas.CollectionPublic, status_code=status.HTTP_201_CREATED)
async def create_new_collection(collection_data: schemas.CollectionCreate):
    # 1. Gera um novo ID
    all_collections = db_json.load_collections()
    new_id = 1
    if all_collections:
        new_id = all_collections[-1].id + 1
    
    # 2. Imagem padrão
    image_url = f"https://via.placeholder.com/300x200/4F518C/FFFFFF?text={collection_data.name}"
    
    # 3. Cria o objeto para salvar
    collection_to_save = schemas.CollectionInDB(
        id=new_id,
        name=collection_data.name,
        is_public=collection_data.is_public,
        owner_id=collection_data.owner_id,
        image_url=image_url,
        value=0.0,      # Garante que começa com 0
        itemCount=0     # Garante que começa com 0
    )
    
    return db_json.create_collection_in_db(collection_to_save)

@router.get("/{user_id}", response_model=List[schemas.CollectionPublic])
async def get_collections_for_user(user_id: int):
    return db_json.get_collections_by_owner_id(user_id)