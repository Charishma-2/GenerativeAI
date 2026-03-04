from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel,Field
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

class summarizeinput_schema(BaseModel):
    user_input: str 
    summary: str = Field(Description="The summary")

#create a node
#node1
def summarize(state: summarizeinput_schema)->summarizeinput_schema:
    curr_user_input = state.user_input
    summary = llm.invoke(f"Summarize the user given input: {curr_user_input}").content
    state.summary = summary
    return state

#node2
def ReturnSummary(state: summarizeinput_schema)->summarizeinput_schema:
    summary = state.summary

    return state

#create a stategraph
graph = StateGraph(summarizeinput_schema)

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
    "user_input":"calculate the sum of 5+5",
    "summary":" "
}))
