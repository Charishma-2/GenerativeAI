from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel,Field
from typing import TypedDict,List
from langgraph.graph import StateGraph, START, END
from IPython.display import Image,display 
from dotenv import load_dotenv
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

#pydantic schema
class graph_schema(BaseModel):
    topic: str = Field(description="The topic of the graph")
    post: str = Field(description="The linkedin post content")
    curated_post: str= Field(description="The curated linkedin post content")


#create a node functions
def create_post(state: graph_schema)->graph_schema:

    
    curr_topic = state.topic
    
    #passing the topic to the llm to generate a linkedin post
    post = llm.invoke(f"write a linkeidn post about the following topic: {curr_topic}").content

    state.post = post

    return state

def curate_post(state: graph_schema)->graph_schema:
    
    curr_post = state.post
    #passing the topic to the llm to generate a linkedin post
    curated_post = llm.invoke(f"curate the following linkeidn post with genz tonw: {curr_post}").content

    state.curated_post = curated_post

    return state

#step-3: create the state graph
graph = StateGraph(graph_schema)

#adding nodes
graph.add_node("firstnode",create_post)
graph.add_node("secondnode",curate_post)

##adding edge
graph.add_edge(START,"firstnode")
graph.add_edge("firstnode","secondnode")
graph.add_edge("secondnode",END)

#step-4: compile my graph
first_graph = graph.compile()

#step-5:run the graph
print(first_graph.invoke({
    "topic":"The importance of data privacy in the digital age",
    "post":" ",
    "curated_post":" "
}))