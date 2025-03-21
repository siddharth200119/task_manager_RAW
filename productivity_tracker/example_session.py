def make_example_session(uname: str) -> str:
    return f"""
Question: Hi

Thought: The user {uname} has greeted me, I should greet back

Answer: Hello, how may I help you?

Question: What are my tasks?

Thought: I need to give the user their tasks

Action: get_task: "{uname}"
PAUSE

Observation: 5 tasks found

Thought: I should tell the user

Answer: There are 5 tasks

Question: Mujhse task updates le lo

Thought: The user has asked me to ask for task updates

Follow Up: hello, do you have any updates?

Observation: yes, i worked 2 hours on 'design footer' today

Thought: I should  log this in time_logs table

Action: excute_query: "INSERT INTO time_logs (user_id, task_id, start_time, notes) VALUES ((SELECT id FROM users WHERE name = '{uname}'))"
PAUSE

Observation: time log entry add in time_logs table

Thought: I should inform the user

Answer: i have added the time log

Question: i want to show princy's tasks

Thought: the user {uname} wants to see princy's tasks

Action: get_task: "{uname}"
PAUSE

Observation: 1 tasks found

Thought: i should tell the user

Answer: i have 1 task

Question:i want to add task for siddharth

Thought: the user {uname} wants to add a task so i need to ask the requirement information like project name,title,description,status,priority and estimated hours

Follow Up: can you tell me the project name,title,description,status,priority and estimated hours

Obdervation: "Website Redesign" "login page" "create login page" "pending" 3 2.0

Action: add_task: "Website Redesign" "login page" "create login page" "pending" 3 2.0
PAUSE

Observation: Task "login page" added to project "Website Redesign"

Thought: Task added successfully, I should inform the user

Answer: I have added the task

Question:i want to add task for princy

Thought: the user {uname} wants to add a task so i need to ask the requirement information like project name,title,description,status,priority and estimated hours

Follow Up: can you tell me the project name,title,description,status,priority and estimated hours

Observation: "Website Redesign" "update footer" "create footer layout" "pending" 2 3.0

Action: add_task: "Website Redesign" "update footer" "create footer layout" "pending" 2 3.0
PAUSE

Observation: Task "update footer" added to project "Website Redesign"

Thought: Task added successfully, I should inform the user

Answer: i have added the task   

Question: Can you add a task to the Website Redesign project?

Thought: The user {uname} wants to add a task to Website Redesign project, so i need to ask the required information like title, description, status, priority and estimated hours

Follow Up: Can you tell me the title, description, status, priority and estimated hours

Observation: "design footer" "create footer layout" "pending" 2 3.0

Action: add_task: "Website Redesign" "design footer" "create footer layout" "pending" 2 3.0
PAUSE

Observation: Task "design footer" added to project "Website Redesign"

Thought: Task added successfully, I should inform the user

Answer: I have added the task

Question: When was the 'design footer' task created?

Thought: The user {uname} wants to know when the 'design footer' task was created, I can use the datetime tool to get the current time as a placeholder or fetch from DB if available

Action: get_datetime: "now"
PAUSE

Observation: "2025-03-19 12:34:56" 

Thought: Since I don’t have direct DB access here, I’ll use the current time as a placeholder. In a real system, I’d query the task’s creation time.

Answer: The 'design footer' task was created around 2025-03-19 12:34:56

Question: Can you add a task without a description?

Thought: The user {uname} wants to add a task without a description

Follow Up: Can you tell me the title, status, priority and estimated hours for the task

Observation: "update links" "pending" 1 2.0

Action: add_task: "Website Redesign" "update links" "" "pending" 1 2.0
PAUSE

Observation: task "update links" added to project "Website Redesign"

Thought: the task was added without a description, I should inform the user

Answer: i have added the task

Question: Can I update the 'design footer' task?

Thought: The user wants to update a task, but I need to know what changes to make

Follow Up: What updates would you like to make to the 'design footer' task? Please provide percentage, hours, and any comments.

Observation: 50.0 2.0 "worked on layout"

Action: update_task: "{uname}" "design footer" 50.0 2.0 "worked on layout"
PAUSE

Observation: task "design footer" updated for {uname}

Thought: task updated successfully, I should inform the user

Answer: i have updated the task

Question: Can you assign a task to a non-existent user?

Thought: The user wants to assign a task to a non-existent user

Action: assign_task: "non existent" "design footer"
PAUSE

Observation: Failed to assign task to user

Thought: The user does not exist, I should inform the user

Answer: You cannot assign the task

Question: Can you assign "update links" to Keval?

Thought: The user {uname} wants to assign a task to another user

Action: assign_task: "Keval" "update links"
PAUSE

Observation: Task assigned to Keval

Thought: task assigned and i should inform the user

Answer: I have assigned the task

Question: Can you update a task with a percentage over 100?

Thought: The user wants to update a task with an invalid percentage

Action: update_task: "{uname}" "design footer" 150.0 1.0 "testing high percentage"
PAUSE

Observation: failed to update this task

Thought: The percentage is invalid and i should inform the user

Answer: You cannot update this task

Question:can you show me all project?

Thought: The user wants to see all projects but I dont have a specific tool for it I should use the SQL tool

Action: get_schema: ""
PAUSE

Obervation: "SCHEMA_IS _RETURNED_HERE"

Thought: I have the schema I can now execute the query to get active projects 

Action: execute_query: "SELECT * FROM projects where status = 'active'"
PAUSE

Observation: "DATA FROM THE DATABASE"

Answer: you have x number of projects like website redesign, etc

"""