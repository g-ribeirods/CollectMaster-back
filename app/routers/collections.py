from fastapi import APIRouter, HTTPException, status
from typing import List
from .. import schemas, db_json

router = APIRouter()

@router.post("/", response_model=schemas.CollectionPublic, status_code=status.HTTP_201_CREATED)
async def create_new_collection(collection_data: schemas.CollectionCreate):
    """
    Cria uma nova coleção para um usuário.
    """
    
    # Lógica simples de ID
    all_collections = db_json.load_collections()
    new_id = len(all_collections) + 1
    
    # (No futuro, você vai querer salvar a imagem aqui)
    image_url = f"https://via.placeholder.com/300x200/4F518C/FFFFFF?text={collection_data.name}"
    
    collection_to_save = schemas.CollectionInDB(
        id=new_id,
        name=collection_data.name,
        is_public=collection_data.is_public,
        owner_id=collection_data.owner_id,
        image_url=image_url,
        value=0.0,
        itemCount=0
    )
    
    created_collection = db_json.create_collection_in_db(collection_to_save)
    return created_collection

@router.get("/{user_id}", response_model=List[schemas.CollectionPublic])
async def get_collections_for_user(user_id: int):
    """
    Busca todas as coleções de um usuário específico.
    """
    collections = db_json.get_collections_by_owner_id(owner_id=user_id)
    if not collections:
        return [] # Retorna lista vazia se não achar nada
    return collections