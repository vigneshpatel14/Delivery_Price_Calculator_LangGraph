import sqlite3
from datetime import datetime

DB_NAME = "delivery.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS delivery_requests
                 (ticket_id TEXT PRIMARY KEY, 
                  user_id TEXT,
                  material_type TEXT,
                  distance REAL,
                  urgency TEXT,
                  weight REAL,
                  location_type TEXT,
                  total_price REAL,
                  status TEXT,
                  created_at TEXT)''')
    
    conn.commit()
    conn.close()

def save_delivery(ticket_id, user_id, material_type, distance, urgency, 
                  weight, location_type, total_price, status):
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''INSERT INTO delivery_requests VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (ticket_id, user_id, material_type, distance, urgency, 
               weight, location_type, total_price, status, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_delivery(ticket_id):

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM delivery_requests WHERE ticket_id = ?', (ticket_id,))
    result = c.fetchone()
    conn.close()
    return result

def get_all_deliveries():
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM delivery_requests ORDER BY created_at DESC')
    results = c.fetchall()
    conn.close()
    return results