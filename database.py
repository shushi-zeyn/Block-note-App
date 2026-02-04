import sqlite3
import datetime
import os

class NoteManager:
    def __init__(self, db_name="notes.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        """Crée la table si elle n'existe pas."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                created_at TEXT,
                updated_at TEXT,
                status TEXT DEFAULT 'En cours'
            )
        ''')
        conn.commit()
        conn.close()

    def add_note(self, title, content, status="En cours"):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        cursor.execute('''
            INSERT INTO notes (title, content, created_at, updated_at, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, content, now, now, status))
        conn.commit()
        conn.close()

    def update_note(self, note_id, title, content, status):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        cursor.execute('''
            UPDATE notes 
            SET title = ?, content = ?, updated_at = ?, status = ?
            WHERE id = ?
        ''', (title, content, now, status, note_id))
        conn.commit()
        conn.close()

    def delete_note(self, note_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
        conn.commit()
        conn.close()

    def get_all_notes(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, created_at, status FROM notes ORDER BY updated_at DESC')
        notes = cursor.fetchall()
        conn.close()
        return notes

    def get_note_content(self, note_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT title, content, status FROM notes WHERE id = ?', (note_id,))
        note = cursor.fetchone()
        conn.close()
        return note
