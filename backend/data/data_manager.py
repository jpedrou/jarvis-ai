import sqlite3
import numpy as np

DB_PATH = "/home/joao/Desktop/facial-agent/backend/data/clients.db"


def insert_client(name, age, image_representation):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO clients (name, age, image_representation) VALUES (?, ?, ?)",
            (name, age, image_representation),
        )
        conn.commit()


def get_all_representations():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT name, image_representation FROM clients")
        rows = c.fetchall()
        return [(row[0], np.frombuffer(row[1], dtype=np.float64)) for row in rows]
