from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('example.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        user_id = request.args.get('id')
        name = request.args.get('name')
        role = request.args.get('role')

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

        return jsonify({
            'status': 'success',
            'users': users,
            'count': len(users)
        }), 200

    except sqlite3.Error as e:
        return jsonify({
            'status': 'error',
            'message': f'Database error: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)