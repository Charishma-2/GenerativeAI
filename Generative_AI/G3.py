from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

chain = llm | JsonOutputParser()

def result(input: str):
    prompt = ChatPromptTemplate.from_template(
        template = 
        """
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
    formatted_prompt = prompt.format(input= input)
    response = chain.invoke(formatted_prompt)
    return response



while True:
    user_input = input("ask:")
    if user_input.lower() in {'exit','quit'}:
        break
    print(result(user_input))



    
