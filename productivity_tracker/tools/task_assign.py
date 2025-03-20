import sqlite3
from RAWW.RAW.tool import Tool

def assign_task(username: str, taskname: str) -> str:
    """
    Assign a task to a user using username and task name.
    
    Args:
        username: Name of the user to assign the task to
        taskname: Title of the task to assign
    
    Returns:
        str: Result message
    """
    print("assign_task tool called successfully.")
    try:
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id FROM users WHERE name = ?
        """, (username,))
        user_result = cursor.fetchone()
        if not user_result:
            raise ValueError(f"User '{username}' not found")
        user_id = user_result[0]
        cursor.execute("""
            SELECT id FROM tasks WHERE title = ?
        """, (taskname,))
        task_result = cursor.fetchone()
        if not task_result:
            raise ValueError(f"Task '{taskname}' not found")
        task_id = task_result[0]
        cursor.execute("""
            SELECT id FROM task_assignments WHERE user_id = ? AND task_id = ?
        """, (user_id, task_id))
        if cursor.fetchone():
            raise ValueError(f"Task '{taskname}' is already assigned to '{username}'")
        cursor.execute("""
            INSERT INTO task_assignments (user_id, task_id, completion_percentage)
            VALUES (?, ?, 0.0)
        """, (user_id, task_id))

        conn.commit()
        
        return f"Task '{taskname}' successfully assigned to '{username}'"

    except Exception as e:
        conn.rollback()
        return f"Failed to assign task: {str(e)}"
    
    finally:
        conn.close()
assign_task_tool = Tool(
    name="assign_task",
    description="Assign a task to a user using their username and task name.",
    action=assign_task,
    example="assign_task \"Siddharth\" \"Project Plan\"",
    test_payloads=[
        "\"Siddharth\" \"Project Plan\"",   
        "\"Keval\" \"Code Review\""       
    ],
    printResult=True
)