from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, collections, items

app = FastAPI()

app.include_router(auth.router, prefix="/api/auth", tags=["Autenticação"])
app.include_router(collections.router, prefix="/api/collections", tags=["Coleções"])
app.include_router(items.router, prefix="/api/items", tags=["Itens"])

origins = [
    "http://localhost:5173",  
    "http://localhost:3000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

app.include_router(
    auth.router, 
    prefix="/api/auth", 
    tags=["Autenticação"]
)

app.include_router(
    collections.router, 
    prefix="/api/collections", 
    tags=["Coleções"]
)
@app.get("/api")
async def root():
    return {"message": "Bem-vindo ao CollectMaster API"}