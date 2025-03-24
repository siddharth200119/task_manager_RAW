from fastapi import FastAPI, HTTPException, BackgroundTasks,Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import subprocess
from dotenv import load_dotenv
import os
import json
from RAWW.RAW import Agent, GroqLLM, OllamaLLM, TextColor, BackgroundColor
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
from datetime import datetime, timedelta
from task_api import get_tasks
from user_api import get_users
from time_logs_api import get_time_logs
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

origins = [
  "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

white_list_copy = json.loads(json.dumps(white_list))

last_message_sent = {number: None for number in white_list} 
last_reply_received = {number: None for number in white_list}  

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

@app.get("/tasks")
async def fetch_tasks(
   task_id: int = None, 
    title: str = None,
    status: str = None,
    priority: int = None
):
    result = get_tasks(task_id, title, status, priority)
    return result

@app.get("/users")
async def fetch_users(
    user_id: int = None,
    name: str = None,
    role: str = None
):
    result = get_users(user_id, name, role)
    return result

@app.get("/time_logs")
async def fetch_time_logs(
    id: int = None,
    task_id: int = None,
    user_id: int = None,
    start_time: str = None,
    end_time: str = None
):
    result = get_time_logs(id, task_id, user_id, start_time, end_time)
    return result


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
            formatted_row = [str(value) if value is not None else 'N/A' for value in row]
            table_row = "<tr>" + "".join(f"<td>{value}</td>" for value in formatted_row) + "</tr>"
            table_rows += table_row
        
        return HTMLResponse(content=html_content.format(table_rows=table_rows))
    
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error: {str(e)}</h1>")

async def process_agent_response(sender: str, message: str):
    """Background task to process agent response and send it asynchronously."""
    if sender not in white_list:
        return
    
    # Update last reply time when a user responds
    last_reply_received[sender] = datetime.now()
    
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

    response = ""
    async for item in white_list[sender](message):
        response = item

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

    background_tasks.add_task(process_agent_response, request.sender, request.message)
    return {"status": "Message received, processing in the background"}

START_TIME = "09:30"
END_TIME = "19:00"

def is_within_schedule():
    """Check if the current time is within the allowed schedule range."""
    now = datetime.now().strftime("%H:%M")
    return START_TIME <= now <= END_TIME

def is_sunday():
    """Check if today is Sunday."""
    return datetime.now().weekday() == 6

def send_message(number, text):
    """Helper function to send a message and log errors."""
    try:
        response = requests.post(
            f"{os.environ.get('COMMS_URL')}/send-message",
            json={"to": number, "text": text}
        )
        response.raise_for_status()
        last_message_sent[number] = datetime.now()  
    except Exception as e:
        print(f"Cannot send message to {white_list_copy[number]}: {str(e)}")

def scheduled_task_initial():
    """Send initial message to all users every 3 hours."""
    if is_sunday() or not is_within_schedule():
        return
    
    for number in white_list:
        send_message(number, f"Hey {white_list_copy[number]}, do you have any updates?")

def scheduled_task_followup():
    """Send follow-up message every 10 minutes to users who haven't replied."""
    if is_sunday() or not is_within_schedule():
        return
    
    current_time = datetime.now()
    for number in white_list:
        last_sent = last_message_sent[number]
        last_reply = last_reply_received[number]
        
        if (last_sent and 
            (last_reply is None or last_reply < last_sent) and 
            (current_time - last_sent) >= timedelta(minutes=10)):
            send_message(number, f"Hey {white_list_copy[number]}, I’m still waiting for your update!")

def evening_task():
    """Task that runs at 7 PM every day except Sundays."""
    if is_sunday():
        return
    send_message("916354879720@c.us", f"Here are the task updates: http://localhost:7991")

# Schedule the tasks
schedule.every(3).hours.do(scheduled_task_initial)  
schedule.every(10).minutes.do(scheduled_task_followup)  
schedule.every().day.at("19:00").do(evening_task)  

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

def start_node_server():
    process = subprocess.Popen(
        ["node", "comms/index.js"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate()
    print("Node.js stdout:", stdout)
    print("Node.js stderr:", stderr)

if __name__ == "__main__":
    start_node_server()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7991)