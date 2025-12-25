# 🔗 Encurtador de URL - Sistema Completo

Sistema completo de encurtamento de URLs com autenticação JWT, desenvolvido com FastAPI (Backend) e Vue.js (Frontend).

## 🚀 Funcionalidades

### Backend (FastAPI)
- ✅ **Autenticação JWT** com Access e Refresh Tokens
- ✅ **Registro de usuários** com hash de senha (bcrypt)
- ✅ **Login seguro** com validação de credenciais
- ✅ **Refresh de tokens** para renovação automática
- ✅ **Criação de URLs encurtadas** por usuário
- ✅ **Listagem de URLs** filtrada por usuário
- ✅ **MongoDB** para persistência de dados

### Frontend (Vue.js)
- ✅ **Páginas de Login e Registro** com design premium
- ✅ **Dashboard** para criar e gerenciar URLs
- ✅ **Interceptor automático** para renovação de tokens
- ✅ **Guards de rota** para proteção de páginas
- ✅ **Design moderno** com glassmorphism e animações
- ✅ **Copiar URL** para área de transferência

## 📋 Pré-requisitos

- Python 3.9+
- Node.js 16+
- MongoDB rodando localmente (porta 27017)

## 🔧 Configuração e Instalação

### Backend

```bash
cd Backend

# Instalar dependências
pip3 install -r requirements.txt

# Configurar variáveis de ambiente (já criado)
# Edite Backend/.env e altere o SECRET_KEY para produção

# Iniciar servidor
python3 -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

O backend estará rodando em: http://127.0.0.1:8000

### Frontend

```bash
cd Frontend/url-shortener-frontend

# Instalar dependências
npm install

# Iniciar servidor de desenvolvimento
npm run dev
```

O frontend estará rodando em: http://localhost:5173 (ou porta similar)

## 🔐 Autenticação JWT

### Tokens
- **Access Token**: Válido por 30 minutos
- **Refresh Token**: Válido por 7 dias

### Endpoints de Autenticação

#### POST `/api/auth/register`
Registra um novo usuário
```json
{
  "email": "user@example.com",
  "password": "senha123"
}
```

#### POST `/api/auth/login`
Autentica usuário e retorna tokens
```json
{
  "email": "user@example.com",
  "password": "senha123"
}
```

Resposta:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

#### POST `/api/auth/refresh`
Renova os tokens usando um refresh token válido
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Endpoints de URLs

#### GET `/api/urls/{user_id}`
Busca todas as URLs de um usuário (requer autenticação)

#### POST `/api/urls/{user_id}`
Cria uma nova URL encurtada (requer autenticação)
```json
{
  "long_url": "https://www.exemplo.com/pagina/muito/longa"
}
```

## 🎨 Características do Design

- **Dark Mode First**: Design escuro moderno e elegante
- **Glassmorphism**: Painéis translúcidos com efeito de vidro
- **Gradientes Vibrantes**: Cores suaves e harmoniosas
- **Animações Fluidas**: Transições e hover effects
- **Responsivo**: Layout adaptável para diferentes telas

## 🔄 Fluxo de Autenticação

1. Usuário faz login → Recebe access_token e refresh_token
2. Access token é armazenado no localStorage
3. Todas as requisições incluem o token no header: `Authorization: Bearer {token}`
4. Se o access token expirar, o sistema automaticamente:
   - Usa o refresh token para obter novos tokens
   - Reexecuta a requisição original
5. Se o refresh token expirar, redireciona para login

## 📁 Estrutura do Projeto

```
Encurtador-Url/
├── Backend/
│   ├── database/
│   │   └── database.py
│   ├── models/
│   │   └── models.py
│   ├── routes/
│   │   ├── auth_router.py
│   │   └── url_router.py
│   ├── utils/
│   │   └── auth.py
│   ├── main.py
│   ├── requirements.txt
│   └── .env
└── Frontend/url-shortener-frontend/
    ├── src/
    │   ├── views/
    │   │   ├── Home.vue
    │   │   ├── Login.vue
    │   │   └── Register.vue
    │   ├── router/
    │   │   └── index.js
    │   ├── services/
    │   │   └── api.js
    │   ├── App.vue
    │   ├── main.js
    │   └── style.css
    └── package.json
```

## 🔒 Segurança

- ✅ Senhas hashadas com bcrypt
- ✅ Tokens JWT assinados com SECRET_KEY
- ✅ Validação de expiração de tokens
- ✅ CORS configurado
- ✅ Separação de access e refresh tokens

## ⚠️ Importante para Produção

Antes de colocar em produção:

1. **Altere o SECRET_KEY** no arquivo `.env`
2. **Configure CORS** para aceitar apenas domínios específicos
3. **Use HTTPS** para todas as comunicações
4. **Configure MongoDB** com autenticação
5. **Use variáveis de ambiente** para configurações sensíveis

## 🎯 Próximos Passos

- [ ] Adicionar estatísticas de cliques
- [ ] Implementar URLs customizadas
- [ ] Adicionar validação de email
- [ ] Implementar redefinição de senha
- [ ] Adicionar paginação na listagem
- [ ] Implementar exclusão de URLs
- [ ] Adicionar testes automatizados

---

Desenvolvido com ❤️ usando FastAPI + Vue.js
