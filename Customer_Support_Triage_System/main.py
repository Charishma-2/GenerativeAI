from fastapi import FastAPI
from pydantic import BaseModel,Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from langgraph.graph import StateGraph, START, END

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature = 0.5)


class User(BaseModel):
    user_input: str

class TraigeResult(BaseModel):
    user_input: str
    ticket_Type: str = Field(None, description="The type of ticket classified by the model")
    ticket_priority: str = Field(None, description="The priority of the ticket classified by the model")
    sentiment: str = Field(None, description="The sentiment of the user input classified by the model")

#creating a nodes for a triage system 
def Ticket_classification(state: TraigeResult)-> TraigeResult:
    curr_user_input = state.user_input

    tickettype = llm.invoke(f"Classify the following user input into one of the following ticket types: 'Technivcal issue', 'Billing issue', 'General inquiry'.  {curr_user_input}").content

    state.ticket_Type = tickettype

    return state

def Sentiment_analysis(state: TraigeResult)-> TraigeResult:
    curr_user_input = state.user_input
    sentiment = llm.invoke(f"Analyze the sentiment of the following user input.ONLY respond with one of the following labels: 'Positive', 'Negative', or 'Neutral'. {curr_user_input}").content

    state.sentiment = sentiment

    return state

def Priority_classification(state: TraigeResult)-> TraigeResult:
    curr_user_input = state.user_input
    priority = llm.invoke(f"Classify the priority of the following user input into one of the following categories: 'High', 'Medium', 'Low'. {curr_user_input}").content

    state.ticket_priority = priority

    return state

#create a stategraph
graph = StateGraph(TraigeResult)

#adding nodes
graph.add_node("ticket_classification", Ticket_classification)
graph.add_node("sentiment_analysis", Sentiment_analysis)
graph.add_node("priority_classification", Priority_classification)

#adding edges
graph.add_edge(START, "ticket_classification")
graph.add_edge("ticket_classification", "sentiment_analysis")
graph.add_edge("sentiment_analysis", "priority_classification")
graph.add_edge("priority_classification", END)

compiled_graph = graph.compile()



@app.post("/triage")
def triage(user: User):
    result = compiled_graph.invoke({"user_input":user.user_input})
    return result