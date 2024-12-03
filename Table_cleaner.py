import sqlite3

def clear_table():
    conn = sqlite3.connect('scores.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM scores')
    conn.commit()
    conn.close()

clear_table()