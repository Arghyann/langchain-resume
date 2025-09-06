import os
import time
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, String, text
from sqlalchemy.orm import declarative_base
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from resumeParser import get_resume_text

load_dotenv()

# ORM setup
Base = declarative_base()

class JobApplication(Base):
    __tablename__ = "job_applications"
    id = Column(String, primary_key=True)
    job_slug = Column(String)
    job_title = Column(String)
    applicant_name = Column(String)
    applicant_email = Column(String)
    expected_salary = Column(String)
    status = Column(String)

# Connect engine
db_url = os.getenv("READ_ONLY_DB_URL")
engine = create_engine(db_url)
db = SQLDatabase(engine)

# Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0,
)

# Toolkit + SQL Agent
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
sql_tools = toolkit.get_tools()

# Resume tool
resume_tool = Tool(
    name="GetResumeText",
    func=get_resume_text,
    description="Fetch the text content of a resume PDF stored in Supabase by file name."
)

# Combine tools
tools = sql_tools + [resume_tool]

# Create agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# System prompt
system_prompt = """
You are a SQL assistant connected to a PostgreSQL database. You can also retrieve and parse resumes stored in a Supabase bucket using the GetResumeText tool. Use this tool to fetch resume text by providing the exact file name of the PDF.
You can also compare resumes and extract relevant information from them.

Rules:
1. Only use SELECT statements. Do not INSERT, UPDATE, DELETE, or DROP.
2. Return plain SQL without Markdown backticks or any code block markers.
3. Return only the minimal query needed.
4. If the request can't be done with SELECT, explain politely.
5. Keep queries safe and efficient.
6. Only use the exact job_title values present in the table.
"""

MAX_MESSAGES = 5  # sliding windows

def main():
    messages = [("system", system_prompt)]

    while True:
        user_query = input("Ask a query: ")
        if not user_query.strip():
            continue

        messages.append(("human", user_query))
        if len(messages) > MAX_MESSAGES + 1:
            messages = [messages[0]] + messages[-MAX_MESSAGES:]

        prompt_text = "\n".join(f"{role}: {msg}" for role, msg in messages)

        try:
            response = agent.invoke({"input": prompt_text})

            # Extract the agent’s final output
            output = response.get("output", "")
            clean_output = output.replace("```sql", "").replace("```", "").strip()

            print("[DEBUG] Agent Output:")
            print(clean_output)

            # Try running if it looks like SQL
            if "select" in clean_output.lower():
                try:
                    with engine.connect() as conn:
                        result = conn.execute(text(clean_output))
                        rows = result.fetchall()
                        print("[DEBUG] Query Results:")
                        for row in rows:
                            print(row)
                except Exception as sql_e:
                    print("[DEBUG] SQL Execution Error:", sql_e)

            messages.append(("assistant", clean_output))

        except Exception as e:
            print("Error:", e)

        time.sleep(0.5)


if __name__ == "__main__":
    main()
