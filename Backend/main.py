from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.url_router import router as url_router
from routes.auth_router import router as auth_router

app = FastAPI()

# Configuração de CORS para o Vue.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, especifique a URL do Vue.js
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")
app.include_router(url_router, prefix="/api")