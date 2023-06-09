import jwt
from config import JWT_SECRET, JWT_ALGORITHM, JWT_EXP_TIME, SALT
from datetime import datetime, timedelta
from passlib.context import CryptContext

def hashpassword(password:str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(password, salt=SALT)
    return hashed_password

def generate_jwt_token(username: str) -> str:
    payload = {
        "username": username,
        "exp": datetime.utcnow() + timedelta(minutes=int(JWT_EXP_TIME))
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

