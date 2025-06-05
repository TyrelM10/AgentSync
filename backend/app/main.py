from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from app.agent import make_graph
import logging
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AgentRequest(BaseModel):
    query: str

async def invoke_agent(query: str):
    logger.info(f"Invoking agent with query: {query}")
    async with make_graph() as graph:
        thread_id = str(uuid.uuid4())
        result = await graph.ainvoke(
            {"messages": [{"role": "user", "content": query}], "retry_count": 0},
            config={"configurable": {"thread_id": thread_id}}
        )
        final_message = result["messages"][-1].content
        logger.info(f"Final response: {final_message}")
        return final_message

@app.post("/agent")
async def agent_endpoint(request: AgentRequest):
    response = await invoke_agent(request.query)
    return {"response": response}