from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import subprocess
from dotenv import load_dotenv
import os
import json
from RAWW.RAW import Agent, GroqLLM,OllamaLLM, TextColor, BackgroundColor
import requests
from white_list import white_list
from example_session import make_example_session
from tools.task_add import task_add_tool
from tools.task_assign import assign_task_tool
from tools.task_update import update_task_tool
from tools.task_get import get_task_tool
from tools.get_schema import get_schema_tool
from tools.execute_query import execute_query_tool
from tools.task_datetime import datetime_tool
import sqlite3
import schedule
import time
import threading
import asyncio
from datetime import datetime

load_dotenv()

app = FastAPI()

white_list_copy = json.loads(json.dumps(white_list))

main_llm = GroqLLM(api_key=os.environ.get("GROQ_API_KEY"))
# main_llm = OllamaLLM(host="http://localhost:11434", model="llama3.1:70b", num_ctx=32768, temperature=0.5)

class MessageRequest(BaseModel):
    sender: str
    message: str
    timestamp: str
    messageId: str

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Schedule Data</title>
</head>
<body>
    <h1>Team Productivity Schedule</h1>
    <div class="table-container">
        <table id="data-table">
            <thead>
                <tr>
                    <th>User ID</th>
                    <th>Name</th>
                    <th>Role</th>
                    <th>Project ID</th>
                    <th>Project Name</th>
                    <th>Project Description</th>
                    <th>Project Start Date</th>
                    <th>Project End Date</th>
                    <th>Project Status</th>
                    <th>Task ID</th>
                    <th>Task Title</th>
                    <th>Task Description</th>
                    <th>Task Status</th>
                    <th>Task Priority</th>
                    <th>Task Created At</th>
                    <th>Task Completed At</th>
                    <th>Estimated Hours</th>
                    <th>Actual Hours</th>
                    <th>Assignment ID</th>
                    <th>Task Assigned At</th>
                    <th>Task Completion %</th>
                    <th>Time Log ID</th>
                    <th>Time Log Start</th>
                    <th>Time Log End</th>
                    <th>Hours Worked</th>
                    <th>Time Log Notes</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
    </div>
</body>
</html>"""

@app.get("/", response_class=HTMLResponse)
async def root():
    try:
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        print("Connected to DB")

        query = """
        SELECT 
            users.id AS user_id,
            users.name AS user_name,
            users.role AS user_role,
            projects.id AS project_id,
            projects.name AS project_name,
            projects.description AS project_description,
            projects.start_date AS project_start_date,
            projects.end_date AS project_end_date,
            projects.status AS project_status,
            tasks.id AS task_id,
            tasks.title AS task_title,
            tasks.description AS task_description,
            tasks.status AS task_status,
            tasks.priority AS task_priority,
            tasks.created_at AS task_created_at,
            tasks.completed_at AS task_completed_at,
            tasks.estimated_hours AS task_estimated_hours,
            tasks.actual_hours AS task_actual_hours,
            task_assignments.id AS assignment_id,
            task_assignments.assigned_at AS task_assigned_at,
            task_assignments.completion_percentage AS task_completion_percentage,
            time_logs.id AS time_log_id,
            time_logs.start_time AS time_log_start,
            time_logs.end_time AS time_log_end,
            time_logs.hours_worked AS time_log_hours,
            time_logs.notes AS time_log_notes
        FROM users
        LEFT JOIN task_assignments ON users.id = task_assignments.user_id
        LEFT JOIN tasks ON task_assignments.task_id = tasks.id
        LEFT JOIN projects ON tasks.project_id = projects.id
        LEFT JOIN time_logs ON tasks.id = time_logs.task_id AND users.id = time_logs.user_id
        ORDER BY users.id, projects.id, tasks.id, time_logs.start_time;
        """
        
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()

        # Generate HTML table rows with all 25 columns
        table_rows = ""
        for row in data:
            # Handle potential None values by replacing with 'N/A' or '0'
            formatted_row = []
            for value in row:
                if value is None:
                    formatted_row.append('N/A')
                else:
                    formatted_row.append(str(value))
            
            # Create table row with all columns
            table_row = "<tr>"
            for value in formatted_row:
                table_row += f"<td>{value}</td>"
            table_row += "</tr>"
            table_rows += table_row
        
        return HTMLResponse(content=html_content.format(table_rows=table_rows))
    
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error: {str(e)}</h1>")
    

async def process_agent_response(sender: str, message: str):
    """Background task to process agent response and send it asynchronously."""
    if sender not in white_list:
        return
    
    # Initialize the agent if not already done
    if not isinstance(white_list[sender], Agent):
        white_list[sender] = Agent(
            name="HEXY",
            role=f"Help employees track their productivity and assist as a general assistant. Right now you are talking to {white_list[sender]}",
            llm=main_llm,
            tools=[task_add_tool, assign_task_tool, update_task_tool, get_task_tool, get_schema_tool, execute_query_tool, datetime_tool],
            textColor=TextColor.GREEN,
            backgroundColor=BackgroundColor.BLACK,
            personality="helpful",
            exampleSession=make_example_session(white_list[sender]),
            allow_follow_up=True
        )

    # Process the agent response
    response = ""
    async for item in white_list[sender](message):
        response = item

    # Send the response to the communication URL
    try:
        requests.post(
            f"{os.environ.get('COMMS_URL')}/send-message",
            json={"to": sender, "text": response}
        )
    except Exception as e:
        print(f"Failed to send message to {sender}: {str(e)}")


@app.post("/chat")
async def chat(request: MessageRequest, background_tasks: BackgroundTasks):
    if request.sender not in white_list:
        raise HTTPException(status_code=400, detail="invalid employee")

    # Add the agent processing to background tasks
    background_tasks.add_task(process_agent_response, request.sender, request.message)

    # Return immediately without waiting for the agent to complete
    return {"status": "Message received, processing in the background"}

import subprocess

START_TIME = "09:30"
END_TIME = "19:00"

def is_within_schedule():
    """Check if the current time is within the allowed schedule range."""
    now = datetime.now().strftime("%H:%M")
    return START_TIME <= now <= END_TIME

def is_sunday():
    """Check if today is Sunday."""
    return datetime.now().weekday() == 6  # 6 represents Sunday

def scheduled_task():
    """Task that runs only within the defined time range and not on Sundays."""
    if is_sunday():
        return
    
    if is_within_schedule():
        for number in white_list:
            try:
                requests.post(f"{os.environ.get('COMMS_URL')}/send-message", json={"to": number, "text": f"Hey {white_list_copy[number]}, do you have any updates?"})
            except:
                print(f"cannot send message to {white_list_copy[number]}")
        return
    else:
        return

def evening_task():
    """Task that runs at 7 PM every day except Sundays."""
    if is_sunday():
        return
    try:
        requests.post(f"{os.environ.get('COMMS_URL')}/send-message", json={"to": "916354879720@c.us", "text": f"Here are the task updates: http://localhost:7991"})
    except:
        print("cannot send message to the user")

# Schedule the tasks
schedule.every(3).hours.do(scheduled_task)
schedule.every().day.at("19:00").do(evening_task)  # Run daily at 7 PM

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep to avoid high CPU usage

# Start scheduler in a background thread
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

def start_node_server():
    process = subprocess.Popen(
        ["node", "comms/index.js"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

if __name__ == "__main__":
    start_node_server()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7991)