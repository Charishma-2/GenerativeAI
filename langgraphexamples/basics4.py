from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from typing import TypedDict,List
from langgraph.graph import StateGraph, START, END
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

prompt = ChatPromptTemplate.from_messages(
    ("system","you are helpful assistant that helps to create and curate posts for social media platform"),
    ("human","I want to create a post about {topic}")
)