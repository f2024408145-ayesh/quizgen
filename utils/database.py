"""
SQLite database for storing quiz history and results.
Db by Ahmad Faizan"
"""

import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "quiz_history.db")


def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS quiz_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            num_questions INTEGER NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            percentage REAL NOT NULL,
            questions_json TEXT NOT NULL,
            answers_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_quiz_result(topic, num_questions, score, total, questions, answers):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        INSERT INTO quiz_sessions
            (topic, num_questions, score, total, percentage, questions_json, answers_json)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        topic,
        num_questions,
        score,
        total,
        round(score / total * 100, 1) if total else 0,
        json.dumps(questions),
        json.dumps(answers),
    ))
    conn.commit()
    last_id = c.lastrowid
    conn.close()
    return last_id


def get_all_sessions():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT id, topic, num_questions, score, total, percentage, created_at
        FROM quiz_sessions
        ORDER BY created_at DESC
    """)
    rows = c.fetchall()
    conn.close()
    return rows


def get_session_detail(session_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT topic, num_questions, score, total, percentage, questions_json, answers_json, created_at
        FROM quiz_sessions WHERE id = ?
    """, (session_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "topic": row[0],
            "num_questions": row[1],
            "score": row[2],
            "total": row[3],
            "percentage": row[4],
            "questions": json.loads(row[5]),
            "answers": json.loads(row[6]),
            "created_at": row[7],
        }
    return None


def delete_session(session_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM quiz_sessions WHERE id = ?", (session_id,))
    conn.commit()
    conn.close()
