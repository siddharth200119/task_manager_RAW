from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('example.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/time_logs', methods=['GET'])
def get_time_logs():
    try:
        id = request.args.get('id') 
        task_id = request.args.get('task_id')
        user_id = request.args.get('user_id')
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')

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
            return jsonify({
                'status': 'error',
                'message': f'No time log found with id {id}'
            }), 404

        return jsonify({
            'status': 'success',
            'time_logs': time_logs,
            'count': len(time_logs)
        }), 200

    except sqlite3.Error as e:
        return jsonify({
            'status': 'error',
            'message': f'Database error: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)