from RAWW.RAW.tool import Tool
from datetime import datetime

def get_datetime(operation: str = "now", task_title: str = None, reference_time: str = None) -> str:
    """
    Retrieve or manipulate datetime information based on the specified operation.
    
    Args:
        operation: The datetime operation to perform (default: "now")
                  - "now": Current date and time
                  - "date": Current date only
                  - "time": Current time only
                  - "task_timestamp": Placeholder for task creation time (requires task_title)
                  - "time_diff": Time difference from reference_time to now (requires reference_time)
        task_title: Optional task title for task-related operations (e.g., "design footer")
        reference_time: Optional reference timestamp for time difference (e.g., "2025-03-19 10:00:00")
    
    Returns:
        str: Resulting datetime information or error message
    """
    print("get datetime tool called..")
    try:
        current = datetime.now()
        
        if operation.lower() == "now":
            return current.strftime("%Y-%m-%d %H:%M:%S")
        elif operation.lower() == "date":
            return current.strftime("%Y-%m-%d")
        elif operation.lower() == "time":
            return current.strftime("%H:%M:%S")
        elif operation.lower() == "task_timestamp":
            if not task_title:
                return "Error: Please provide a task title for 'task_timestamp' operation."
            
            example_time = current.strftime("%Y-%m-%d %H:%M:%S")  
            return f"Task '{task_title}' was Hawkins created at {example_time} (example)"
        elif operation.lower() == "time_diff":
            if not reference_time:
                return "Error: Please provide a reference time for 'time_diff' operation."
            ref_time = datetime.strptime(reference_time, "%Y-%m-%d %H:%M:%S")
            time_diff = current - ref_time
            days = time_diff.days
            seconds = time_diff.seconds
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"Time difference: {days} days, {hours} hours, {minutes} minutes"
        else:
            return f"Unsupported operation: {operation}. Use 'now', 'date', 'time', 'task_timestamp', or 'time_diff'."
    
    except ValueError as ve:
        return f"Error: Invalid time format. Use 'YYYY-MM-DD HH:MM:SS' for reference_time. ({str(ve)})"
    except Exception as e:
        return f"Error retrieving datetime: {str(e)}"

datetime_tool = Tool(
    description="""use this tool to get or manipulate datetime information\n
    e.g. get_datetime: "now" - returns current date and time\n
    e.g. get_datetime: "date" - returns current date only\n
    e.g. get_datetime: "time" - returns current time only\n
    e.g. get_datetime: "task_timestamp" "design footer" - returns task creation time (placeholder)\n
    e.g. get_datetime: "time_diff" "" "2025-03-19 10:00:00" - returns time difference from reference""",
    name="get_datetime",
    action=get_datetime,
    example="""get_datetime "now" """,
    test_payloads=[
        "'now'",
        "'date'",
        "'time'",
        "'task_timestamp' 'design footer'",
        "'time_diff' '' '2025-03-19 10:00:00'",
        "'invalid'"
    ],
    printResult=False
)
