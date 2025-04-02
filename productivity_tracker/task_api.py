from fastapi import HTTPException
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('example.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_tasks(
    task_id: int = None, 
    title: str = None,
    status: str = None,
    priority: int = None
):
    try:
        query = "SELECT id, title, status, priority FROM tasks WHERE 1=1"
        params = []

        if task_id:
            query += " AND id = ?"
            params.append(task_id)
        if title:
            query += " AND title = ?"
            params.append(title)
        if status:
            query += " AND status = ?"
            params.append(status)
        if priority:
            query += " AND priority = ?"
            params.append(priority)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        tasks = [dict(task) for task in cursor.fetchall()]
        
        conn.close()

        return {
            'status': 'success',
            'tasks': tasks,
            'count': len(tasks)
        }
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')
