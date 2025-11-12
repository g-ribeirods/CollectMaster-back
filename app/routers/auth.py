from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, security, db_json

router = APIRouter()

@router.post("/register", response_model=schemas.UserPublic, status_code=status.HTTP_201_CREATED)
async def register_user(user: schemas.UserCreate):
    
    db_user = db_json.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado",
        )
    
    hashed_password = security.get_password_hash(user.password)
    
    all_users = db_json.load_users()
    new_id = len(all_users) + 1
    
    user_to_save = schemas.UserInDB(
        id=new_id,
        name=user.name,
        email=user.email,
        hashed_password=hashed_password
    )
    
    created_user = db_json.create_user(user_to_save)

    return created_user