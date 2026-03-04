from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import streamlit as st
from dotenv import load_dotenv
load_dotenv()


st.title("Langchain Demo with GeminiAI API")
input_text = st.text_input("Search the topic you want")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

prompt = ChatPromptTemplate.from_messages([
    ("system","you are a helpful assistant.Please response to the user queries"),
    ("human", "Question:{Question}")
])

chain = prompt | llm | StrOutputParser()

if input_text:
    st.write(chain.invoke({'Question':input_text}))