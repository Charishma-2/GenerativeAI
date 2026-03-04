from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

class promptinput(BaseModel):
    text: str

class Shape(BaseModel):
    shape: str
    height: int
    radius: int 

prompt = ChatPromptTemplate.from_template(
        template="""
       tou have to extract the shape and dimension from the user provided sentence.
        Return ONLY valid JSON.
        example:
        user input = create a square with sides 4cm
        output:
        {{
            "shape": "square",
            "side": 4
        }}

        Sentence: {input}
        """
)

chain = prompt | llm | JsonOutputParser()

@app.get("/")
def greet():
    return {'message':'Hello welcome'}
@app.get("/summarize")
def summarize(text: str):
    response = chain.invoke({"input": text})
    return response

@app.post("/summarize")
def summarize(data: promptinput):
    response = chain.invoke({"input": data.text})
    return response

