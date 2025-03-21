from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('example.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    try:
        task_id = request.args.get('id')
        title = request.args.get('title')
        status = request.args.get('status')
        priority = request.args.get('priority')

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

        return jsonify({
            'status': 'success',
            'tasks': tasks,
            'count': len(tasks)
        }), 200

    except sqlite3.Error as e:
        return jsonify({
            'status': 'error',
            'message': f'Database error: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)