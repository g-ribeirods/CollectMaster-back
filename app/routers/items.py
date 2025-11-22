from fastapi import APIRouter, HTTPException, status
from typing import List
from .. import schemas, db_json

router = APIRouter()

@router.post("/", response_model=schemas.ItemPublic, status_code=status.HTTP_201_CREATED)
async def create_new_item(item_data: schemas.ItemCreate):
    # 1. Gerar ID
    all_items = db_json.load_items()
    new_id = 1 if not all_items else all_items[-1].id + 1
    
    # 2. Imagem Placeholder
    image_url = f"https://via.placeholder.com/150?text={item_data.name}"

    # 3. Criar objeto
    item_to_save = schemas.ItemInDB(
        id=new_id,
        image_url=image_url,
        **item_data.model_dump()
    )
    
    return db_json.create_item_in_db(item_to_save)

@router.get("/collection/{collection_id}", response_model=List[schemas.ItemPublic])
async def get_items(collection_id: int):
    return db_json.get_items_by_collection_id(collection_id)

@router.put("/{item_id}", response_model=schemas.ItemPublic)
async def update_item(item_id: int, item_update: schemas.ItemUpdate):
    updated_item = db_json.update_item_in_db(item_id, item_update)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return updated_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    success = db_json.delete_item_in_db(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return None