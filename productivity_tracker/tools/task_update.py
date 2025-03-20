import sqlite3
from datetime import datetime
from RAWW.RAW.tool import Tool

def update_task(username: str, taskname: str, completion_percentage: float, hours_worked: float, notes: str = "") -> str:
    """
    Update a task's assignment and log time worked.
    
    Args:
        username: Name of the user assigned to the task
        taskname: Title of the task to update
        completion_percentage: New completion percentage (0.0 to 100.0)
        hours_worked: Hours worked to log
        notes: Optional notes for the time log (default: "")
    
    Returns:
        str: Result message
    """
    print("update_task tool called successfully.")
    conn=None
    try:
        completion_percentage = float(completion_percentage)
        hours_worked = float(hours_worked)
        
        if not 0.0 <= completion_percentage <= 100.0:
            raise ValueError("Completion percentage must be between 0.0 and 100.0")
        if hours_worked < 0:
            raise ValueError("Hours worked cannot be negative")

        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE name = ?", (username,))
        user_result = cursor.fetchone()
        if not user_result:
            raise ValueError(f"User '{username}' not found")
        user_id = user_result[0]
        cursor.execute("SELECT id FROM tasks WHERE title = ?", (taskname,))
        task_result = cursor.fetchone()
        if not task_result:
            raise ValueError(f"Task '{taskname}' not found")
        task_id = task_result[0]

        cursor.execute("SELECT id FROM task_assignments WHERE user_id = ? AND task_id = ?", 
                      (user_id, task_id))
        assignment_result = cursor.fetchone()
        if not assignment_result:
            raise ValueError(f"Task '{taskname}' is not assigned to '{username}'")

        cursor.execute("""
            UPDATE task_assignments 
            SET completion_percentage = ?
            WHERE user_id = ? AND task_id = ?
        """, (completion_percentage, user_id, task_id))

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("""
            INSERT INTO time_logs (task_id, user_id, start_time, end_time, hours_worked, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (task_id, user_id, current_time, current_time, hours_worked, notes))

        conn.commit()
        return f"Task '{taskname}' updated for '{username}': {completion_percentage}% complete, {hours_worked} hours logged"

    except Exception as e:
        if conn:
            conn.rollback()
        return f"Failed to update task: {str(e)}"
    
    finally:
        if conn:
            conn.close()
update_task_tool = Tool(
    name="update_task",
    description="Update a task's completion percentage and log time worked using username and task name.",
    action=update_task,
    example="update_task \"Siddharth\" \"Project Plan\" 50.0 2.5 \"Updated timeline\"",
    test_payloads=[
        "\"Siddharth\" \"Project Plan\" 50.0 2.5 \"Progress update\"",  
        "\"Keval\" \"Code Review\" 75.0 1.5 \"Code checked\""                           
    ],
    printResult=True
)