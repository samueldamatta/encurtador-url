from fastapi import APIRouter, HTTPException, responses
from models.models import UrlCreate, UrlInDB
from database.database import urls_collection
from typing import List
from utils.utils import generate_hash_short_code
from datetime import datetime

router = APIRouter(prefix="/urls", tags=["urls"])

@router.get("/{user_id}", response_model=List[UrlInDB], status_code=200)
async def get_urls_by_user(user_id: str):
    try:
        print("Buscando todas as URLs...")
        urls = list(urls_collection.find({"user_id": user_id}, {"_id": 0}))
        return urls
    except Exception as e:
        print(f"Erro ao buscar URLs: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar urls")

@router.post("/{user_id}", response_model=UrlInDB)
async def create_short_url(user_id: str, url_data: UrlCreate):
    try:
        print(f"Recebida requisição para encurtar: {url_data.long_url}")
        
        # Gera o short_code usando a função de hash
        short_code = generate_hash_short_code(url_data.long_url)
        
        # Verifica se a URL já foi encurtada anteriormente
        existing_url = urls_collection.find_one({"id": short_code}, {"_id": 0})
        if existing_url:
            print(f"URL já existe: {short_code}")
            return existing_url

        # Cria o novo objeto para o banco de dados
        new_url = {
            "id": short_code,
            "long_url": url_data.long_url,
            "created_at": datetime.now(),
            "user_id": user_id
        }
        
        # Insere no MongoDB
        urls_collection.insert_one(new_url)
        
        # Remove o _id do dicionário antes de retornar para evitar erro de serialização
        if "_id" in new_url:
            del new_url["_id"]
            
        print(f"URL criada com sucesso: {short_code}")
        return new_url
    except Exception as e:
        print(f"Erro ao criar URL: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{short_code}")
async def redirect_to_long_url(short_code: str):
    try:
        print(f"Redirecionando: {short_code}")
        url_doc = urls_collection.find_one({"id": short_code})
        if url_doc:
            return responses.RedirectResponse(url=url_doc["long_url"])
        raise HTTPException(status_code=404, detail="URL não encontrada")
    except Exception as e:
        print(f"Erro no redirecionamento: {e}")
        raise HTTPException(status_code=500, detail="Erro interno")