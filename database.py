import sqlite3
import json

DB_NAME = 'quiz.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            options TEXT NOT NULL,
            correct_option_id INTEGER NOT NULL,
            is_sent INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def add_question(question: str, options: list, correct_option_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Check if question already exists to prevent duplicates
    cursor.execute('SELECT id FROM questions WHERE question = ?', (question,))
    if cursor.fetchone():
        conn.close()
        return False

    cursor.execute('''
        INSERT INTO questions (question, options, correct_option_id, is_sent)
        VALUES (?, ?, ?, 0)
    ''', (question, json.dumps(options, ensure_ascii=False), correct_option_id))
    
    conn.commit()
    conn.close()
    return True

def get_unsent_question():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Get a random unsent question
    cursor.execute('SELECT id, question, options, correct_option_id FROM questions WHERE is_sent = 0 ORDER BY RANDOM() LIMIT 1')
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            'id': row[0],
            'question': row[1],
            'options': json.loads(row[2]),
            'correct_option_id': row[3]
        }
    return None

def mark_as_sent(question_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE questions SET is_sent = 1 WHERE id = ?', (question_id,))
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM questions')
    total = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM questions WHERE is_sent = 1')
    sent = cursor.fetchone()[0]
    conn.close()
    return {'total': total, 'sent': sent, 'unsent': total - sent}

# Bazani yaratish (fayl birinchi marta ishlaganda)
init_db()
