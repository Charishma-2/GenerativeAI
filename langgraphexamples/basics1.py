from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from IPython.display import Image,display 
from dotenv import load_dotenv
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

#step-1: Define the schema
class graph_schema(TypedDict):
    name: str
    message:str

#step-2: create the node functions
def welcome(state: graph_schema) -> graph_schema:
    curr_name = state['name']
    curr_message = state['message']
    
    response = llm.invoke(f"my name is {curr_name} {curr_message}").content

    state['message'] = f"your message was {curr_message}. here is my responses: {response}"

    return state

#step-3: create the state graph
graph =  StateGraph(graph_schema)
#adding nodes
graph.add_node("welcome",welcome)

#adding edge
graph.add_edge(START,"welcome")
graph.add_edge("welcome",END)

#step-4: compile my graph
pydantic_graph = graph.compile()

display(Image(pydantic_graph.get_graph().draw_mermaid()))

#step-5:run the graph
print(pydantic_graph.invoke({"name":"cherry","message": "How are you"}))