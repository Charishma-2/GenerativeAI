from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel,Field
from typing import TypedDict,List
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

#pydantic schema
class graph_schema(BaseModel):
    user_input: str
    summary: str = Field(description="The summary")

#create a node
#node1
def summarize(state: graph_schema)->graph_schema:
    curr_user_input = state.user_input
    if len(curr_user_input) >50 :
        summary = llm.invoke(f"Summarize the user given input: {curr_user_input}").content
        state.summary = summary
        return state
    
    else:
        state.user_input = curr_user_input
        return state

def ReturnSummary(state: graph_schema)->graph_schema:
    summary = state.summary

    return state

#create a stategraph
graph = StateGraph(graph_schema)

#adding nodes
graph.add_node("firstnode",summarize)
graph.add_node("secondnode",ReturnSummary)

#adding edges
graph.add_edge(START,"firstnode")
graph.add_edge("firstnode","secondnode")
graph.add_edge("secondnode",END)

#step-4: compile my graph
first_graph = graph.compile()

#step-5:run the graph
print(first_graph.invoke({
    "user_input":"Yes, you can use a length function, but it depends on the programming language or environment you are using. The idea is straightforward: you measure the number of characters (or tokens, depending on your requirement) in the input string.",
    "summary":" "
}))

