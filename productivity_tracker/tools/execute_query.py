from RAWW.RAW import Tool
import sqlite3

def execute_query(query: str):
    try:
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        
        # Execute the query
        cursor.execute(query)
        
        # Fetch results if it's a SELECT query
        if query.strip().lower().startswith("select"):
            result = cursor.fetchall()
        else:
            conn.commit()  # Commit changes for INSERT, UPDATE, DELETE
            result = "Query executed successfully."
        
        # Close the connection
        conn.close()
        
        return str(result)

    except Exception as e:
        return str(e)

execute_query_tool = Tool(
    name="execute_query",
    description="use this tool to get the schema of the database",
    action=execute_query,
    example=""" "SELECT * FROM TABLE_NAME" """
)