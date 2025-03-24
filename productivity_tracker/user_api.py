from fastapi import HTTPException
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('example.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_users(
    user_id: int = None,
    name: str = None,
    role: str = None
):
    try:
        query = "SELECT id, name, role FROM users WHERE 1=1"
        params = []

        if user_id:
            query += " AND id = ?"
            params.append(user_id)
        if name:
            query += " AND name = ?"
            params.append(name)
        if role:
            query += " AND role = ?"
            params.append(role)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        users = [dict(user) for user in cursor.fetchall()]
        
        conn.close()

        return {
            'status': 'success',
            'users': users,
            'count': len(users)
        }
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')