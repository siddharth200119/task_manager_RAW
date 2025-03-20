# Database Schema Documentation

## Overview
This document describes the schema of the SQLite database used to track team productivity. It includes tables for users, projects, tasks, task assignments, time logs, milestones, performance metrics, and comments.

## Tables

### users
Stores information about team members.

| Column Name | Data Type | Constraints          | Description            |
|-------------|-----------|----------------------|------------------------|
| id          | INTEGER   | PRIMARY KEY, AUTOINCREMENT | Unique user identifier |
| name        | TEXT      | NOT NULL            | User's name            |
| role        | TEXT      | NOT NULL            | User's role            |

### projects
Organizes tasks into projects.

| Column Name | Data Type | Constraints          | Description                  |
|-------------|-----------|----------------------|------------------------------|
| id          | INTEGER   | PRIMARY KEY, AUTOINCREMENT | Unique project identifier    |
| name        | TEXT      | NOT NULL            | Project name                 |
| description | TEXT      |                      | Project details              |
| start_date  | TIMESTAMP |                      | Project start date           |
| end_date    | TIMESTAMP |                      | Project end date (optional)  |
| status      | TEXT      | NOT NULL, DEFAULT 'active' | Project status (active, completed, on_hold) |

### tasks
Stores individual tasks with productivity tracking fields.

| Column Name    | Data Type | Constraints          | Description                  |
|----------------|-----------|----------------------|------------------------------|
| id             | INTEGER   | PRIMARY KEY, AUTOINCREMENT | Unique task identifier       |
| project_id     | INTEGER   | FOREIGN KEY          | Associated project           |
| title          | TEXT      | NOT NULL            | Task name                    |
| description    | TEXT      |                      | Task details                 |
| status         | TEXT      | NOT NULL, DEFAULT 'pending' | Task status (pending, in_progress, completed) |
| priority       | INTEGER   | NOT NULL, DEFAULT 1  | Priority (1-5, 5 is highest) |
| created_at     | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation time           |
| completed_at   | TIMESTAMP |                      | Completion time              |
| estimated_hours| REAL      |                      | Estimated hours to complete  |
| actual_hours   | REAL      |                      | Actual hours spent           |

### task_assignments
Tracks which users are assigned to which tasks.

| Column Name      | Data Type | Constraints          | Description                  |
|------------------|-----------|----------------------|------------------------------|
| id              | INTEGER   | PRIMARY KEY, AUTOINCREMENT | Unique assignment identifier |
| user_id         | INTEGER   | NOT NULL, FOREIGN KEY | User assigned to task        |
| task_id         | INTEGER   | NOT NULL, FOREIGN KEY | Task being assigned          |
| assigned_at     | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Assignment time         |
| completion_percentage | REAL | DEFAULT 0.0         | Progress (0.0 to 100.0)      |

### time_logs
Records time spent on tasks for detailed productivity analysis.

| Column Name  | Data Type | Constraints          | Description                  |
|--------------|-----------|----------------------|------------------------------|
| id           | INTEGER   | PRIMARY KEY, AUTOINCREMENT | Unique time log identifier   |
| task_id      | INTEGER   | NOT NULL, FOREIGN KEY | Task being worked on         |
| user_id      | INTEGER   | NOT NULL, FOREIGN KEY | User logging time            |
| start_time   | TIMESTAMP | NOT NULL            | Start of work session        |
| end_time     | TIMESTAMP |                      | End of work session          |
| hours_worked | REAL      |                      | Calculated hours (optional)  |
| notes        | TEXT      |                      | Optional notes about work    |

## Sample Data
- **users**: Siddharth, Keval, Princy as Team Leads
- **projects**: Website Redesign, API Development
- **tasks**: Project Plan, Code Review, Documentation
- **task_assignments**: Links users to tasks with progress
- **time_logs**: Sample time entries for tasks

## Last Updated
March 16, 2025