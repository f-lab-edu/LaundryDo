from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from config import APIConfigurations


pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "65cea85d36060df1841ba5689840b0da447100ed823ab7e3b610c447c9a497d0" # create using openssl rand -hex 32
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = f'/v{APIConfigurations.version}/login')