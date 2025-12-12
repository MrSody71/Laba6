from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

conn = sqlite3.connect("notes.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, text TEXT)")
conn.commit()

class Note(BaseModel):
    text: str

@app.post("/add")
def add_note(note: Note):
    cursor.execute("INSERT INTO notes (text) VALUES (?)", (note.text,))
    conn.commit()
    return {"status": "added"}

@app.get("/list")
def list_notes():
    cursor.execute("SELECT id, text FROM notes")
    return cursor.fetchall()
