from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer
import jwt

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")

class Security:
  oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

  @staticmethod
  def get_password_hash(password):
    return password_hash.hash(password)
  
  @staticmethod
  def verify_password(password, hashed_password):
    return password_hash.verify(password, hashed_password)
  
  @staticmethod
  def encode_jwt(to_encode, secret_key, algorithm):
    encodes = jwt.encode(to_encode, secret_key, algorithm)
    return encodes