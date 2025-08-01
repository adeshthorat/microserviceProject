from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
conn.commit()

class User(BaseModel):
    name: str
    email: str

@app.post("/users")
def create_user(user: User):
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (user.name, user.email))
    conn.commit()
    return {"message": "User added successfully"}

@app.get("/users")
def get_users():
    cursor.execute("SELECT * FROM users")
    return [{"id": row[0], "name": row[1], "email": row[2]} for row in cursor.fetchall()]
