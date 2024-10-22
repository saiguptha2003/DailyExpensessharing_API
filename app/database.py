import sqlite3
import hashlib
import json
from datetime import datetime

def init_db():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        mobile TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        description TEXT NOT NULL,
        amount REAL NOT NULL,
        split_type TEXT NOT NULL,
        split_data TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    )
    ''')

    conn.commit()
    conn.close()

def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()

def addUser(name, email, mobile, password):
    hashedPassword = hashPassword(password)
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT INTO users (name, email, mobile, password)
        VALUES (?, ?, ?, ?)
        ''', (name, email, mobile, hashedPassword))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error: Email already exists.")
    finally:
        conn.close()

def getUserByEmail(email):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return {
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "mobile": user[3],
            "password": user[4]
        }
    return None

def getUserById(userId):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE id = ?', (userId,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return {
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "mobile": user[3],
            "password": user[4]
        }
    return None

def addExpenseToDB(user_email, description, amount, split_type, split_data):
    user = getUserByEmail(user_email)
    if not user:
        print("Error: User not found.")
        return

    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    slitDataJson = json.dumps(split_data)

    try:
        cursor.execute('''
        INSERT INTO expenses (user_id, description, amount, split_type, split_data)
        VALUES (?, ?, ?, ?, ?)
        ''', (user['id'], description, amount, split_type, slitDataJson))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

def getUserExpenses(user_id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM expenses WHERE user_id = ?', (user_id,))
    expenses = cursor.fetchall()
    conn.close()

    return [{
        "id": exp[0],
        "user_id": exp[1],
        "description": exp[2],
        "amount": exp[3],
        "split_type": exp[4],
        "split_data": json.loads(exp[5]),  
        "created_at": exp[6]
    } for exp in expenses]

def getAllExpenses():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM expenses')
    expenses = cursor.fetchall()
    conn.close()

    return [{
        "id": exp[0],
        "user_id": exp[1],
        "description": exp[2],
        "amount": exp[3],
        "split_type": exp[4],
        "split_data": json.loads(exp[5]), 
        "created_at": exp[6]
    } for exp in expenses]

def verifyUserCredentials(email, password):
    user = getUserByEmail(email)
    if user and user['password'] == hashPassword(password):
        return user
    return None
