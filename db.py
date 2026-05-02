import sqlite3

conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS groups (
    chat_id INTEGER PRIMARY KEY,
    interval INTEGER DEFAULT 3600
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER,
    chat_id INTEGER,
    points INTEGER DEFAULT 0,
    PRIMARY KEY (user_id, chat_id)
)
""")

conn.commit()


def add_group(chat_id):
    cursor.execute("INSERT OR IGNORE INTO groups(chat_id) VALUES(?)", (chat_id,))
    conn.commit()


def get_groups():
    cursor.execute("SELECT chat_id, interval FROM groups")
    return cursor.fetchall()


def set_interval(chat_id, interval):
    cursor.execute("UPDATE groups SET interval=? WHERE chat_id=?", (interval, chat_id))
    conn.commit()


def add_points(user_id, chat_id, points=1):
    cursor.execute("""
    INSERT INTO users(user_id, chat_id, points)
    VALUES (?, ?, ?)
    ON CONFLICT(user_id, chat_id)
    DO UPDATE SET points = points + ?
    """, (user_id, chat_id, points, points))
    conn.commit()


def get_ranking(chat_id):
    cursor.execute("""
    SELECT user_id, points FROM users
    WHERE chat_id=?
    ORDER BY points DESC LIMIT 5
    """, (chat_id,))
    return cursor.fetchall()
