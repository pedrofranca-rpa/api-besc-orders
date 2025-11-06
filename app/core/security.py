import hashlib
from fastapi.responses import JSONResponse
import jwt
from datetime import datetime, timedelta
from app.core.config import settings
from fastapi import HTTPException, Request
from jwt import decode, exceptions

from fastapi import Request, HTTPException
from jwt import decode, exceptions


def hash_password(password: str) -> str:
    """Gera hash SHA256 para armazenar a senha com segurança."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """Compara senha fornecida com hash armazenado."""
    return hash_password(password) == password_hash


def create_access_token(subject: str) -> str:
    """Cria um token JWT com validade de 12 horas."""
    payload = {"sub": subject, "exp": datetime.utcnow() + timedelta(hours=12)}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str):
    """Decodifica o token JWT e retorna o payload."""
    try:
        return jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
    except jwt.PyJWTError:
        return None


EXCLUDED_PATHS = [
    "/api/users/register",
    "/api/users/login",
    "/docs",
    "/openapi.json",
    "/health",
]


async def jwt_middleware(request: Request, call_next):
    """Middleware que exige JWT em todas as rotas (exceto as públicas)."""
    if any(request.url.path.startswith(path) for path in EXCLUDED_PATHS):
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=401,
            content={"detail": "Token ausente ou inválido"},
        )

    token = auth_header.split(" ")[1]

    try:
        decode(token, settings.JWT_SECRET, algorithms=["HS256"])
    except exceptions.ExpiredSignatureError:
        return JSONResponse(status_code=401, content={"detail": "Token expirado"})
    except exceptions.DecodeError:
        return JSONResponse(status_code=401, content={"detail": "Token inválido"})
    except Exception as e:
        return JSONResponse(
            status_code=401, content={"detail": f"Erro no token: {str(e)}"}
        )

    response = await call_next(request)
    return response
