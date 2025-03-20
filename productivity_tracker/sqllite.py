import sqlite3
import json
import os

def setup_database():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        INSERT OR IGNORE INTO users (name, role) VALUES
        ('Siddharth', 'Team Lead'),
        ('Keval', 'Team Lead'),
        ('Princy', 'Team Lead'),
        ('Gopi','Team Member'),
        ('Dinkey','Team Member'),
        ('Sneha','Team Member'),
        ('Dhaval','Team Member'),
        ('Parth Frontend','Team Member'),
        ('Vivek','Team Member'),
        ('Umesh','Team Member'),
        ('Rishit','Team Member'),
        ('Rutvik','Team Member'),
        ('Syrin','Team Member'),
        ('Nakul','Team Member'),
        ('Harsh','Team Member'),
        ('Dhruvi','Team Member'),
        ('Parth AIML','Team Member'),
        ('Parth Cyber','Team Member'),
        ('Honey','Team Member')
        
    ''')

    # Projects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            start_date TIMESTAMP,
            end_date TIMESTAMP,
            status TEXT NOT NULL DEFAULT 'active'
        )
    ''')
    cursor.execute('''
        INSERT OR IGNORE INTO projects (name, description, start_date, status) VALUES
        ('Website Redesign', 'Revamp company website', '2025-03-01', 'active'),
        ('API Development', 'Build new API endpoints', '2025-03-10', 'active')
    ''')

    # Tasks table (updated with project_id)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'pending',
            priority INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            estimated_hours REAL,
            actual_hours REAL,
            FOREIGN KEY (project_id) REFERENCES projects(id)
        )
    ''')
    cursor.execute('''
        INSERT OR IGNORE INTO tasks (project_id, title, description, status, priority, estimated_hours) VALUES
        (1, 'Project Plan', 'Create initial project timeline', 'pending', 3, 4.0),
        (1, 'Code Review', 'Review team code submissions', 'in_progress', 2, 2.5),
        (2, 'Documentation', 'Write API documentation', 'completed', 1, 3.0)
    ''')

    # Task assignments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS task_assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            task_id INTEGER NOT NULL,
            assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completion_percentage REAL DEFAULT 0.0,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (task_id) REFERENCES tasks(id),
            UNIQUE(user_id, task_id)
        )
    ''')
    cursor.execute('''
        INSERT OR IGNORE INTO task_assignments (user_id, task_id, completion_percentage) VALUES
        (1, 1, 0.0),
        (2, 2, 50.0),
        (3, 3, 100.0)
    ''')

    # Time logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS time_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            start_time TIMESTAMP NOT NULL,
            end_time TIMESTAMP,
            hours_worked REAL,
            notes TEXT,
            FOREIGN KEY (task_id) REFERENCES tasks(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    cursor.execute('''
        INSERT OR IGNORE INTO time_logs (task_id, user_id, start_time, end_time, hours_worked, notes) VALUES
        (2, 2, '2025-03-15 09:00:00', '2025-03-15 11:00:00', 2.0, 'Initial review'),
        (3, 3, '2025-03-14 10:00:00', '2025-03-14 13:00:00', 3.0, 'Completed draft')
    ''')

    # Milestones table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS milestones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            due_date TIMESTAMP NOT NULL,
            completed_at TIMESTAMP,
            status TEXT NOT NULL DEFAULT 'pending',
            FOREIGN KEY (project_id) REFERENCES projects(id)
        )
    ''')
    cursor.execute('''
        INSERT OR IGNORE INTO milestones (project_id, name, due_date, status) VALUES
        (1, 'Design Phase Complete', '2025-03-20', 'pending'),
        (2, 'API v1 Release', '2025-03-25', 'pending')
    ''')

    # Performance metrics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS performance_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            period_start TIMESTAMP NOT NULL,
            period_end TIMESTAMP NOT NULL,
            tasks_completed INTEGER DEFAULT 0,
            avg_completion_time REAL,
            efficiency_score REAL,
            on_time_percentage REAL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Comments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            comment TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (task_id) REFERENCES tasks(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    cursor.execute('''
        INSERT OR IGNORE INTO comments (task_id, user_id, comment) VALUES
        (1, 1, 'Need clarification on scope'),
        (2, 2, 'Found some bugs to fix')
    ''')

    conn.commit()
    conn.close()

# Function to get schema from markdown file
def get_schema():
    try:
        schema_file_path = os.path.join(os.path.dirname(__file__), "schema.md")
        
        if not os.path.exists(schema_file_path):
            raise FileNotFoundError("Schema Markdown file not found")
        
        with open(schema_file_path, 'r', encoding='utf-8') as f:
            schema_content = f.read()
        
        return schema_content
    except Exception as e:
        raise Exception(f"Error getting schema: {str(e)}")

# Function to execute query
def execute_query(query: str):
    try:
        if not query.strip().lower().startswith("select"):
            raise ValueError("Only SELECT queries are allowed")
        
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return {"results": results}
    except Exception as e:
        raise Exception(f"Error executing query: {str(e)}")
if __name__ == "__main__":
    setup_database()
    print("Database created successfully!")