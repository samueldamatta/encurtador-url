from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a URI do MongoDB
MONGO_URI = os.getenv("MONGO_URI")

# Inicializa o cliente do MongoDB com um timeout de 5 segundos
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

# Seleciona o banco de dados
db = client["url_shortener"]

# Define as coleções
urls_collection = db["urls"]
users_collection = db["users"]

