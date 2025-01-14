from pydantic import BaseModel
class ChatCreate(BaseModel):
    conversation: str

class Chat(ChatCreate):
    id: int


class ChatRequest(BaseModel):
    message: str
    userId: int

class ChatResponse(BaseModel):
    response: str

class ChatUpdateRequest(BaseModel):
    chat_id: int
    updated_conversation: str