import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

# check if api key is present
if not os.getenv("GOOGLE_API_KEY"):
    print("Error: GOOGLE_API_KEY not found. Please add it to your .env file.")
    exit(1)

from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor

# ... (Previous imports kept, but we re-write the bottom part)

# 1. Define a Tool
@tool
def multiply(a: int, b: int) -> int:
    """Multiplies two numbers."""
    return a * b

# 2. Setup Tools
tools = [multiply]

# 3. Initialize Model with Tools
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# 4. Create Agent
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use your tools to answer math questions."),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 5. Run
user_input = "What is 5 times 8?"
print(f"User: {user_input}")

try:
    response = agent_executor.invoke({"input": user_input})
    print(f"Agent: {response['output']}")
except Exception as e:
    print(f"Error: {e}")
