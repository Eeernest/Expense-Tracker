from pydantic import BaseModel

class TokenBase(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  id: int