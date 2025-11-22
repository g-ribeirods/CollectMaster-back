from fastapi import APIRouter, HTTPException, status
from typing import List
from .. import schemas, db_json

router = APIRouter()

@router.post("/", response_model=schemas.CollectionPublic, status_code=status.HTTP_201_CREATED)
async def create_new_collection(collection_data: schemas.CollectionCreate):
    all_collections = db_json.load_collections()
    new_id = 1 if not all_collections else all_collections[-1].id + 1
    
    # Usa a imagem enviada OU um placeholder se estiver vazia
    final_image = collection_data.image_url or f"https://via.placeholder.com/300x200/4F518C/FFFFFF?text={collection_data.name}"
    
    collection_to_save = schemas.CollectionInDB(
        id=new_id,
        name=collection_data.name,
        description=collection_data.description, # Novo
        is_public=collection_data.is_public,
        owner_id=collection_data.owner_id,
        image_url=final_image,
        value=0.0,
        itemCount=0
    )
    
    return db_json.create_collection_in_db(collection_to_save)

# NOVO ENDPOINT DE ATUALIZAÇÃO
@router.put("/{collection_id}", response_model=schemas.CollectionPublic)
async def update_collection(collection_id: int, collection_update: schemas.CollectionUpdate):
    updated_col = db_json.update_collection_in_db(collection_id, collection_update)
    if not updated_col:
        raise HTTPException(status_code=404, detail="Coleção não encontrada")
    return updated_col

@router.get("/{user_id}", response_model=List[schemas.CollectionPublic])
async def get_collections_for_user(user_id: int):
    return db_json.get_collections_by_owner_id(user_id)