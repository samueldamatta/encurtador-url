from fastapi import APIRouter, HTTPException, status
from models.models import UserCreate, UserLogin, UserInDB, User, Token, RefreshTokenRequest
from database.database import users_collection
from utils.auth import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    create_refresh_token,
    verify_token
)
import uuid

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate):
    """
    Registra um novo usuário no sistema

    """
    # Verifica se o email já existe
    existing_user = users_collection.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já está em uso"
        )
    
    # Cria o hash da senha
    hashed_password = get_password_hash(user_data.password)
    
    # Cria o novo usuário
    user_id = str(uuid.uuid4())
    new_user = {
        "id": user_id,
        "email": user_data.email,
        "password": hashed_password
    }
    
    # Insere no banco de dados
    users_collection.insert_one(new_user)
    
    # Retorna o usuário sem a senha
    return User(id=user_id, email=user_data.email)


@router.post("/login", response_model=Token)
async def login(user_data: UserLogin):
    """
    Autentica um usuário e retorna access e refresh tokens

    """
    # Busca o usuário pelo email
    user = users_collection.find_one({"email": user_data.email})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Verifica a senha
    if not verify_password(user_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Cria os tokens
    access_token = create_access_token(data={"sub": user["id"], "email": user["email"]})
    refresh_token = create_refresh_token(data={"sub": user["id"]})
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(token_data: RefreshTokenRequest):
    """
    Renova os tokens usando um refresh token válido
    
    Args:
        token_data: Refresh token
    
    Returns:
        Token: Novos access e refresh tokens
    
    Raises:
        HTTPException 401: Se o refresh token for inválido ou expirado
    """
    # Verifica o refresh token
    payload = verify_token(token_data.refresh_token, token_type="refresh")
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    user_id = payload.get("sub")
    
    # Verifica se o usuário ainda existe
    user = users_collection.find_one({"id": user_id})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Cria novos tokens
    access_token = create_access_token(data={"sub": user["id"], "email": user["email"]})
    refresh_token = create_refresh_token(data={"sub": user["id"]})
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )