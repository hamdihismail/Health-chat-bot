from pydantic import BaseModel
class UserCreate(BaseModel):
    username: str
    password: str

class User(UserCreate):
    id: int

class UserResponse(BaseModel):
    id: int
    username: str