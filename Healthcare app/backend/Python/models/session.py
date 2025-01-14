from pydantic import BaseModel
class SessionCreate(BaseModel):
    userId: int
    chatId: int

class Session(SessionCreate):
    id: int