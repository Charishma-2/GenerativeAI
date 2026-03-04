from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str

@app.get("/greet")
def greet_user_get(name: str):
    return {"message": "Hello, " + name + "!"}

@app.post("/greet")
def greet_user(name: str):
    return {"message": "Hello, "+name+"!"}