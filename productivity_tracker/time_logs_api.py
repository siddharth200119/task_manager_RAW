from fastapi import HTTPException
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('example.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_time_logs(
    id: int = None,
    task_id: int = None,
    user_id: int = None,
    start_time: str = None,
    end_time: str = None
):
    try:
        query = "SELECT id, task_id, user_id, start_time, end_time, hours_worked, notes FROM time_logs WHERE 1=1"
        params = []

        if id:
            query = "SELECT id, task_id, user_id, start_time, end_time, hours_worked, notes FROM time_logs WHERE id = ?"
            params = [id]
        else:
            if task_id:
                query += " AND task_id = ?"
                params.append(task_id)
            if user_id:
                query += " AND user_id = ?"
                params.append(user_id)
            if start_time:
                query += " AND start_time >= ?"
                params.append(start_time)
            if end_time:
                query += " AND end_time <= ?"
                params.append(end_time)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        time_logs = [dict(log) for log in cursor.fetchall()]
        
        conn.close()

        if not time_logs and id:
            raise HTTPException(status_code=404, detail=f'No time log found with id {id}')

        return {
            'status': 'success',
            'time_logs': time_logs,
            'count': len(time_logs)
        }
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')