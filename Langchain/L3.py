from langchain.tools import tool
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
load_dotenv()

#setup the LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

#math function
@tool("Calculator",description="Peform all the math functions asked by the user")
def calculate(expression: str)->str:
    """
    Evaluate basic math expressions like 5+5, 10*2, or (8/2)+1.
    """
    result = eval(expression)
    return str(result)

#created an agent
agent = create_agent(llm,tools=[calculate])


while(True):
    user_input = input("ask: ")
    if user_input.lower() in {"quit","exit"}:
        break
    print(llm.invoke(user_input).content)