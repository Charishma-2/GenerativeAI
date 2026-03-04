from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel,Field
from langchain.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from typing import Literal
from dotenv import load_dotenv
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)


class Route(BaseModel):
    type: Literal["math", "text"] = Field(
        None, description="The next step in the routing process"
    )
router = llm.with_structured_output(Route)

class graph_schema(BaseModel):
    user_input: str
    result : str 
    check: str

def llm_call_router(state: graph_schema):
    decision = router.invoke(
        [
            SystemMessage(content="check the user input is either math or text"),
            HumanMessage(content=state.user_input)
        ]
    )
    return {"check": decision.type}

def condition(state: graph_schema):
    if state.check == "math":
        return "math_calculate"
    else:
        return "text_evaluate"



def math_calculate(state: graph_schema)->graph_schema:
    curr_user_input=state.user_input
    
    result = llm.invoke(
        f"""
        Convert the following text into a valid Python math expression.
        Return ONLY the expression.

        Input: {curr_user_input}
        """
    ).content.strip()

    state.result = result

    return state

def text_evaluate(state: graph_schema)->graph_schema:
    curr_user_input = state.user_input

    result = llm.invoke(f"you are a helpful assistant .please respond to user input: {curr_user_input}").content

    state.result = result

    return state




#create a stategraph
graph = StateGraph(graph_schema)

#adding nodes

graph.add_node("math_calculate",math_calculate)
graph.add_node("text_evaluate",text_evaluate)
graph.add_node("llm_call_router",llm_call_router)



#adding edges
graph.add_edge(START,"llm_call_router")
graph.add_conditional_edges(
    "llm_call_router",
    condition,
    {"text_evaluate":"text_evaluate","math_calculate":"math_calculate"}
)
graph.add_edge("text_evaluate",END)
graph.add_edge("math_calculate",END)

router_graph = graph.compile()

#step-5:run the graph
print(router_graph.invoke({
    "user_input":"divide 4 with 2",
    "result":" ",
    "check":" "
    
}))
