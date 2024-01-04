from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from config import APIConfigurations
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY=os.getenv('SECRET_KEY', 'NONE')
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = f'/v{APIConfigurations.version}/login')