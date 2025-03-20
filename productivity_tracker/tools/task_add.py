# from RAWW import Tool
import sqlite3
from RAWW.RAW.tool import Tool

def add_task(project_name: str, title: str, description: str = "", 
             status: str = "pending", priority: int = 1, 
             estimated_hours: float = 0.0) -> str:
    """
    Add a new task to a project using project name instead of ID.
    
    Args:
        project_name: Name of the project
        title: Task title
        description: Task description
        status: Task status (default: 'pending')
        priority: Task priority (default: 1)
        estimated_hours: Estimated hours for completion (default: 0.0)
    
    Returns:
        str: Result message
    """
    print("add_task tool called Successfully...")
    try:
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        print("Connected_to_db")
        
        cursor.execute("""
            SELECT id FROM projects 
            WHERE name LIKE ? AND status = 'active'
        """, (f'%{project_name}%',))
         
        project_result = cursor.fetchone()
        print("Project result:", project_result)
        if not project_result:
            raise ValueError(f"Project '{project_name}' not found or not active")
        
        project_id = project_result[0]

        cursor.execute("""
            INSERT INTO tasks (project_id, title, description, status, priority, estimated_hours)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (project_id, title, description, status, priority, estimated_hours))

        conn.commit()
        print("Query Executed Successfully...")
        
        return f"Task '{title}' successfully added to project '{project_name}'"

    except Exception as e:
        conn.rollback()
        return f"Failed to add task: {str(e)}"
    
    finally:
        conn.close()

task_add_tool = Tool(
    name="add_task",
    description="Add a new task to a project using the project name.",
    action=add_task,
    example="add_task \"Website Redesign\" \"New Task\" \"Task description\" \"pending\" 2 3.5",
    test_payloads=[
        "\"Website Redesign\" \"Test Task 1\" \"This is a test\" \"pending\" 2 3.0",
        "\"API Development\" \"Test Task 2\" \"\" \"in_progress\" 1 2.5",
        "\"Non Existent Project\" \"Test Task 3\" \"Should fail\" \"pending\" 1 1.0"
    ],
    printResult=True
)


