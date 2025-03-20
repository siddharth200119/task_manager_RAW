from RAWW.RAW import Tool

def get_schema(*args):
    try:
        with open("schema.md", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "schema.md file not found."

get_schema_tool = Tool(
    name="get_schema",
    description="use this tool to get the schema of the database",
    action=get_schema,
    example=""" "" """
)