from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0.2)

class prompt(BaseModel):
    text: str

class Shape(BaseModel):
    shape: str
    height: int
    radius: int

prompts = ChatPromptTemplate.from_template(
    template = 
    """
    take the shape and dimensions from the user input.
    return only json format only.
    sentence:{input}
    """
)

chain = prompts | llm | JsonOutputParser()

@app.get("/")
def greet():
    return "Its working"

@app.get("/summarize")
def summarize(text: str):
    response = chain.invoke({'input':text})
    return response

@app.post("/summarize")
def summarize(text: prompt):
    response = chain.invoke({'input':text.text})
    return response

