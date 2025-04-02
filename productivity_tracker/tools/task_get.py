import sqlite3
from RAWW.RAW.tool import Tool

def get_task(username: str) -> str:
    """
    Retrieve all tasks assigned to a user by their username.
    
    Args:
        username: Name of the user whose tasks are to be retrieved
    
    Returns:
        str: Result message with the list of tasks or an error
    """
    print("get_task tool called sucessfully.")
    try:
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE name = ?", (username,))
        user_result = cursor.fetchone()
        if not user_result:
            raise ValueError(f"User '{username}' not found")
        user_id = user_result[0]

        cursor.execute("""
            SELECT t.title 
            FROM tasks t
            JOIN task_assignments ta ON t.id = ta.task_id
            WHERE ta.user_id = ?
        """, (user_id,))
        tasks = cursor.fetchall()

        if not tasks:
            return f"No tasks found for '{username}'"
        
        task_list = [task[0] for task in tasks]
        task_count = len(task_list)
        task_str = ", ".join(task_list)
        return f"{task_count} tasks found for '{username}': {task_str}"

    except Exception as e:
        return f"Failed to retrieve tasks: {str(e)}"
    
    finally:
        conn.close()

get_task_tool = Tool(
    name="get_task",
    description="Retrieve all tasks assigned to a user by their username.",
    action=get_task,
    example="get_task \"Siddharth\"",
    test_payloads=[
        "\"Siddharth\"",
        "\"Keval\"",
        "\"NonexistentUser\""
    ],
    printResult=True
)

