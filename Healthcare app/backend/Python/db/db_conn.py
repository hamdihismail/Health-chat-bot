import os
import sqlite3
from typing import List
from models import user, chat, session
User = user.User
UserCreate = user.UserCreate
Chat = chat.Chat
ChatCreate = chat.ChatCreate
Session = session.Session
SessionCreate = session.SessionCreate

path = "/home / User / Desktop / file.txt"
start = "/home / User"

def create_connection():
 connection = sqlite3.connect("C:\\Users\\user\\desktop\\healthcare app\\backend\\Python\\db\\chat.db")
 return connection

def db_init():
    conn = create_connection()
    sql_statements = [
        '''CREATE TABLE IF NOT EXISTS user
                    (id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL);''',
        '''CREATE TABLE IF NOT EXISTS chat
                    (id INTEGER PRIMARY KEY, conversation TEXT);''',
        '''CREATE TABLE IF NOT EXISTS session (
                id INTEGER PRIMARY KEY, 
                userId INTEGER NOT NULL,                    
                chatId INTEGER NOT NULL,
                FOREIGN KEY (userId)
                    REFERENCES user (id)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE, 
                FOREIGN KEY (chatId)
                    REFERENCES chat (id)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE
                );''',
        '''CREATE TRIGGER IF NOT EXISTS delete_user_sessions
           AFTER DELETE ON user
           FOR EACH ROW
           BEGIN
            DELETE FROM session
            WHERE userId = OLD.id;
           END;''',
           '''CREATE TRIGGER IF NOT EXISTS delete_user_chats
           AFTER DELETE ON user
           FOR EACH ROW
           BEGIN            
            DELETE FROM chat
            WHERE id IN (
                SELECT chatId FROM session WHERE userId = OLD.id
            );
           END;''',
           '''CREATE TRIGGER IF NOT EXISTS delete_chat_sessions
           AFTER DELETE ON chat
           FOR EACH ROW
           BEGIN
            DELETE FROM session
            WHERE chatId = OLD.id;
           END;'''
    ]

    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    for statement in sql_statements:
        cur.execute(statement)
    conn.commit()
    cur.close()

def db_get_all_users() -> List[User]:
    conn = create_connection()
    sql = '''SELECT * FROM user'''
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    users = [User(id=row[0], username=row[1], password=row[2]) for row in rows]
    return users

def db_get_user(id: int) -> User:
    conn = create_connection()
    sql = '''SELECT * FROM user WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql,(id,))
    row = cur.fetchone()
    cur.close()
    if row:
        return User(id=row[0], username=row[1], password=row[2])
    else:
        return None
def db_get_user_by_name(username: str) -> User:
    conn = create_connection()
    sql = '''SELECT * FROM user WHERE username = ?'''
    cur = conn.cursor()
    cur.execute(sql,(username,))
    row = cur.fetchone()
    cur.close()
    if row:
        return User(id=row[0], username=row[1], password=row[2])
    else:
        return None

def db_delete_user(id):
    conn = create_connection()
    sql = '''DELETE FROM user WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql,(id,))
    conn.commit()
    cur.close()

def db_save_user(user: UserCreate):
    conn = create_connection()
    sql = '''INSERT INTO user(username,password)
        VALUES(?,?)'''
    cur = conn.cursor()
    cur.execute(sql,(user.username,user.password))
    conn.commit()
    user_id = cur.lastrowid
    cur.close()
    conn.close()
    return user_id


def db_get_all_chats():
    conn = create_connection()
    sql = '''SELECT * FROM chat'''
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    chats = [{"id": row[0], "conversation": row[1]} for row in rows]
    return chats

def db_get_chat_by_id(chat_id: int):
    conn = create_connection()
    sql = '''SELECT * FROM chat WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (chat_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        return {"id": row[0], "conversation": row[1]}
    return None

def db_get_chats_by_user(user_id: int):
    conn = create_connection()
    sql = '''
        SELECT chat.id, chat.conversation 
        FROM chat
        JOIN session ON chat.id = session.chatId
        WHERE session.userId = ?
    '''
    cur = conn.cursor()
    cur.execute(sql, (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    chats = [{"id": row[0], "conversation": row[1]} for row in rows]
    return chats

def db_save_chat(chat: ChatCreate):
    conn = create_connection()
    sql = '''INSERT INTO chat(conversation)
        VALUES(?)'''
    cur = conn.cursor()
    cur.execute(sql,[chat.conversation])
    conn.commit()
    chat_id = cur.lastrowid
    cur.close()
    return chat_id

def db_delete_chat_by_id(chat_id: int) -> bool:
    conn = create_connection()
    sql = '''DELETE FROM chat WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (chat_id,))
    conn.commit()
    rows_affected = cur.rowcount
    cur.close()
    conn.close()

    return rows_affected > 0

def db_update_conversation(chat_id: int, updated_conversation: str):
    conn = create_connection()
    sql = '''UPDATE chat SET conversation = ? WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (updated_conversation, chat_id,))
    conn.commit()
    cur.close()


def db_get_all_sessions():
    conn = create_connection()
    sql = '''SELECT * FROM session'''
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    sessions = [{"id": row[0], "userId": row[1], "chatId": row[2]} for row in rows]
    return sessions

def db_get_sessions_by_user(user_id: int):
    conn = create_connection()
    sql = '''SELECT * FROM session WHERE userId = ?'''
    cur = conn.cursor()
    cur.execute(sql, (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    sessions = [{"id": row[0], "userId": row[1], "chatId": row[2]} for row in rows]
    return sessions

def db_get_sessions_by_id(id: int):
    conn = create_connection()
    sql = '''SELECT * FROM session WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    sessions = [{"id": row[0], "userId": row[1], "chatId": row[2]} for row in rows]
    return sessions

def db_save_session(session: SessionCreate):
    conn = create_connection()
    sql = '''INSERT INTO session(userId,chatId)
        VALUES(?,?)'''
    cur = conn.cursor()
    cur.execute(sql,(session.userId,session.chatId))
    conn.commit()
    session_id = cur.lastrowid
    cur.close()
    return session_id

def db_delete_session_by_id(session_id: int) -> bool:
    conn = create_connection()
    sql = '''DELETE FROM session WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (session_id,))
    conn.commit()
    rows_affected = cur.rowcount
    cur.close()
    conn.close()

    return rows_affected > 0

db_init()