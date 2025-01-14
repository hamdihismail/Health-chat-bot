import sqlite3
from db import db_conn
from typing import Union,List
from models import user, chat, session
from services import chat_service
chatService = chat_service.main
User = user.User
UserCreate = user.UserCreate
Chat = chat.Chat
ChatCreate = chat.ChatCreate
ChatRequest = chat.ChatRequest
ChatResponse = chat.ChatResponse
ChatUpdateRequest = chat.ChatUpdateRequest
Session = session.Session
SessionCreate = session.SessionCreate

from fastapi import FastAPI, HTTPException

db = db_conn
app = FastAPI()

conn = db.create_connection()

# User endpoints

@app.get("/users/user/{id}", response_model=User)
def get_single_user(id:int):
    user = db.db_get_user(id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/login", response_model=User, response_model_exclude={"password"})
def login(user_login: UserCreate):
    user = db.db_get_user_by_name(user_login.username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.password != user_login.password:
        raise HTTPException(status_code=401, detail="Username or password does not match our records")
    return user

@app.get("/users/all", response_model=List[User])
def get_all_users():
    users = db.db_get_all_users()
    if users is None:
        raise HTTPException(status_code=404, detail="No users not found")
    return users
@app.post("/users/add")

def create_user_endpoint(user: UserCreate):
    try:
        user_id = db.db_save_user(user)
        return {"id": user_id, **user.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.delete("/users/{id}")
def delete_user_endpoint(id:int):
    try:
        db.db_delete_user(id)
        return "Successfuly removed user"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# Chat endpoints

@app.post("/chat/{sessionId}", response_model=ChatResponse)
def chat_endpoint(chat_request: ChatRequest,sessionId:int):
    # Call the refactored main function with continuous conversation support
    response = chatService(chat_request.message, chat_request.userId,sessionId)
    
    # Return the response from the main function to the frontend
    return {"response": response}

@app.get("/chat/all", response_model=List[Chat])
def get_all_chats():
    return db.db_get_all_chats()

@app.get("/chat/{chat_id}", response_model=Chat)
def get_chat_by_id(chat_id: int):
    chat = db.db_get_chat_by_id(chat_id)
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat

@app.get("/chat/user/{user_id}", response_model=List[Chat])
def get_chats_by_user(user_id: int):
    return db.db_get_chats_by_user(user_id)

@app.post("/chat/add")
def create_chat_endpoint(chat: ChatCreate):
    try:
        chat_id = db.db_save_chat(chat)
        return {"id": chat_id, **chat.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/chat/update", response_model=ChatResponse)
def update_conversation(chat_update: ChatUpdateRequest):
    try:
        db.db_update_conversation(chat_update.chat_id, chat_update.updated_conversation)
        return {"response": f"Chat with ID {chat_update.chat_id} updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/chat/{chat_id}", response_model=dict)
def delete_chat(chat_id: int):
    success = db.db_delete_chat_by_id(chat_id)
    if not success:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"detail": "Chat deleted successfully"}


# Session endpoints
@app.get("/session/all", response_model=List[Session])
def get_all_sessions():
    return db.db_get_all_sessions()


@app.get("/session/{id}", response_model=List[Session])
def get_sessions_by_user(id: int):
    return db.db_get_sessions_by_id(id)

@app.get("/session/user/{user_id}", response_model=List[Session])
def get_sessions_by_user(user_id: int):
    return db.db_get_sessions_by_user(user_id)

@app.post("/session/add")
def create_session_endpoint(session: SessionCreate):
    try:
        session_id = db.db_save_session(session)
        return {"id": session_id, **session.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/session/{session_id}", response_model=dict)
def delete_session(session_id: int):
    success = db.db_delete_session_by_id(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"detail": "Session deleted successfully"}