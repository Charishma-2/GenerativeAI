from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()


class TextIn(BaseModel):
    text: str


def count_words(text: str)-> int:
    return len(text.split())


@app.get("/summarize")
def word_count_user(text: str):
    return {"word_count":  count_words(text)}


@app.post("/summarize")
def word_count(txt: TextIn):
    return {"word_count": count_words(txt.text)}