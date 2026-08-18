import sqlite3
from datetime import datetime

DB_NAME = "finmind_research.db"

def init_db():
    """Initializes the SQLite database and creates a history table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT,
            company_name TEXT,
            price REAL,
            pe_ratio TEXT,
            sentiment TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_search_record(ticker, company_name, price, pe_ratio, sentiment):
    """Saves a research search query and its core metrics into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Handle P/E ratio conversion safely for database storage
    pe_val = str(pe_ratio)
    
    cursor.execute('''
        INSERT INTO search_history (ticker, company_name, price, pe_ratio, sentiment, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (ticker, company_name, price, pe_val, sentiment, timestamp))
    
    conn.commit()
    conn.close()

def get_search_history():
    """Retrieves past search history records from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT ticker, company_name, price, sentiment, timestamp FROM search_history ORDER BY id DESC LIMIT 10')
    records = cursor.fetchall()
    conn.close()
    return records