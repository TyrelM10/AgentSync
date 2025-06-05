# from langchain_ollama import ChatOllama
# from langgraph.graph import StateGraph, START, END
# from langchain_mcp_adapters.client import MultiServerMCPClient
# from langchain_core.messages import HumanMessage, AIMessage
# import asyncio
# from typing import TypedDict, Annotated
# from langgraph.graph.message import add_messages
# from langgraph.prebuilt import ToolNode, tools_condition

# class State(TypedDict):
#     messages: Annotated[list, add_messages]

# async def create_agent():
#     model = ChatOllama(model="llama3.2:1b", temperature=0)
    
#     async with MultiServerMCPClient({
#         "gmail": {"command": "python", "args": ["app/mcp_servers/gmail_server.py"], "transport": "stdio"},
#         # "linear": {"command": "python", "args": ["app/mcp_servers/linear_server.py"], "transport": "stdio"},
#         # "notion": {"command": "python", "args": ["app/mcp_servers/notion_server.py"], "transport": "stdio"},
#         # "slack": {"command": "python", "args": ["app/mcp_servers/slack_server.py"], "transport": "stdio"},
#     }) as client:
#         tools = client.get_tools()
#         llm_with_tools = model.bind_tools(tools)
        
#         def chatbot(state: State):
#             return {"messages": [llm_with_tools.invoke(state["messages"])]}
        
#         graph_builder = StateGraph(State)
#         graph_builder.add_node("chatbot", chatbot)
#         graph_builder.add_node("tools", ToolNode(tools=tools))
#         graph_builder.add_conditional_edges("chatbot", tools_condition)
#         graph_builder.add_edge("tools", "chatbot")
#         graph_builder.set_entry_point("chatbot")
#         graph = graph_builder.compile()
#         return graph

# async def invoke_agent(query: str):
#     graph = await create_agent()
#     result = await graph.ainvoke({"messages": [HumanMessage(content=query)]})
#     return result["messages"][-1].content

# ------------ ONLY SENDING MAILS USING GMAIL APPLICATION --------------
'''
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_send_email():
    async with MultiServerMCPClient({
        "gmail": {"command": "python", "args": ["app/mcp_servers/gmail_server.py"], "transport": "stdio"},
    }) as client:
        tools = client.get_tools()
        logger.info(f"Available tools: {[tool.name for tool in tools]}")
        
        if not tools:
            logger.error("No tools available")
            return
        for tool in tools:
            print(tool.name)
        send_email_tool = next((tool for tool in tools if tool.name == "send_email"), None)
        if not send_email_tool:
            logger.error("send_email tool not found")
            return
        
        try:
            logger.info("Invoking send_email tool")
            result = await send_email_tool.ainvoke({
                "recipient": "tjmenezes08@gmail.com",
                "subject": "TEST",
                "body": "Hello Mate I am your Agent."
            })
            logger.info(f"Tool result: {result}")
        except Exception as e:
            logger.error(f"Error invoking tool: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_send_email())
'''
'''
from contextlib import asynccontextmanager
from typing import Annotated, Sequence, TypedDict
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
import logging
import asyncio
from anyio import ClosedResourceError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    retry_count: int

@asynccontextmanager
async def make_graph():
    system_prompt = (
        "You are an assistant that exclusively uses the `send_email` tool to send emails via Gmail. "
        "For any email-related query, invoke the `send_email` tool with `recipient`, `subject`, and `body` parameters. "
        "Do NOT suggest or generate code using `smtplib`, other libraries, or alternative methods, even if errors occur. "
        "If an error occurs, report it and retry the `send_email` tool."
    )
    llm = ChatOllama(model="llama3.2:3b", temperature=0, system=system_prompt)

    mcp_client = MultiServerMCPClient({
        "gmail": {
            "command": "python",
            "args": ["app/mcp_servers/gmail_server.py"],
            "transport": "stdio",
        }
    })

    async with mcp_client:
        mcp_tools = mcp_client.get_tools()
        logger.info(f"Available tools: {[tool.name for tool in mcp_tools]}")
        llm_with_tools = llm.bind_tools(mcp_tools)

        async def agent(state: State):
            logger.info(f"Processing messages: {[msg.content for msg in state['messages']]}, Retry count: {state.get('retry_count', 0)}")
            messages = state["messages"]
            response = await llm_with_tools.ainvoke(messages)
            logger.info(f"LLM response: {response}")
            if response.content and "smtplib" in response.content.lower():
                logger.warning("LLM generated smtplib response; overriding to retry tool")
                return {
                    "messages": [response],
                    "retry_count": state.get("retry_count", 0) + 1
                }
            return {"messages": [response], "retry_count": state.get("retry_count", 0)}

        graph_builder = StateGraph(State)
        graph_builder.add_node("agent", agent)
        graph_builder.add_node("tools", ToolNode(mcp_tools))

        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges(
            "agent",
            tools_condition,
            {
                "tools": "tools",
                END: END,
            }
        )
        graph_builder.add_edge("tools", "agent")

        # Use MemorySaver for state persistence, requiring thread_id in configurable
        graph = graph_builder.compile(checkpointer=MemorySaver())
        graph.name = "Email Agent"

        yield graph
'''
# ----------- CONNECTING TO LINEAR APPLICATION ------------
'''
from contextlib import asynccontextmanager
from typing import Annotated, Sequence, TypedDict
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import BaseMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
import logging
import asyncio
from anyio import ClosedResourceError
import json
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    retry_count: int

@asynccontextmanager
async def make_graph():
    system_prompt = (
        "You are an assistant that uses two tools: `send_email` and `create_linear_issue`. "
        "For email-related queries, invoke `send_email` with parameters: `recipient` (string), `subject` (string), `body` (string). "
        "For Linear-related queries (e.g., creating tasks or issues), invoke `create_linear_issue` with parameters: `title` (string), `description` (string), `project_id` (string), `team_id` (string). "
        "The `team_id` is REQUIRED for creating Linear issues. For example: "
        "`create_linear_issue(title='Sample Task', description='This is a test issue.', project_id='9d542fc5-44d8-45cb-8a59-fda8f503ed79', team_id='your_team_id')`. "
        "DO NOT wrap parameters in a `fields` object or JSON structure like `{'fields': {...}}`. "
        "If the query provides `title`, `description`, and `project_id` but omits `team_id`, respond with: 'Please provide the team ID to create the Linear issue.' "
        "If a GraphQL error indicates 'Field \"teamId\" of required type \"String!\" was not provided', prompt for `team_id`. "
        "DO NOT claim an issue was created unless the API confirms success. "
        "DO NOT suggest or generate code using `smtplib`, other libraries, or alternative methods. "
        "Retry up to 3 times if an error occurs. If retries fail, return a clear error message. "
        "If the query doesn't require a tool, respond directly with a concise answer."
    )
    llm = ChatOllama(model="llama3.2:3b", temperature=0, system=system_prompt)

    mcp_client = MultiServerMCPClient({
        "gmail": {
            "command": "python",
            "args": ["app/mcp_servers/gmail_server.py"],
            "transport": "stdio",
        },
        "linear": {
            "command": "python",
            "args": ["app/mcp_servers/linear_server.py"],
            "transport": "stdio",
        }
    })

    async with mcp_client:
        mcp_tools = mcp_client.get_tools()
        logger.info(f"Available tools: {[tool.name for tool in mcp_tools]}")
        llm_with_tools = llm.bind_tools(mcp_tools)

        async def agent(state: State):
            logger.info(f"Processing messages: {[msg.content for msg in state['messages']]}, Retry count: {state.get('retry_count', 0)}")
            messages = state["messages"]
            retry_count = state.get("retry_count", 0)

            if retry_count >= 3:
                logger.error("Max retries exceeded for tool call")
                return {
                    "messages": [AIMessage(content="Unable to process request with tools. Please try again or provide the required team ID.")],
                    "retry_count": retry_count
                }

            response = await llm_with_tools.ainvoke(messages)
            logger.info(f"LLM response: {response}")

            # Check for invalid response (no tool calls, smtplib mention, or GraphQL error)
            if response.content and ("smtplib" in response.content.lower() or not response.tool_calls):
                logger.warning(f"LLM generated invalid response: {response.content}")

                # Check for missing teamId in user input or GraphQL error
                if "teamId" in response.content.lower() or any("Field \"teamId\" of required type \"String!\" was not provided" in msg.content for msg in messages):
                    logger.info("Detected missing teamId")
                    return {
                        "messages": [AIMessage(content="Please provide the team ID to create the Linear issue.")],
                        "retry_count": retry_count
                    }

                # Attempt to parse malformed JSON-like response
                try:
                    if "fields" in response.content:
                        parsed = json.loads(response.content)
                        if "fields" in parsed and all(key in parsed["fields"] for key in ["title", "description", "project_id"]):
                            logger.info("Correcting malformed fields object to tool call")
                            corrected_tool_call = {
                                "name": "create_linear_issue",
                                "args": {
                                    "title": parsed["fields"]["title"],
                                    "description": parsed["fields"]["description"],
                                    "project_id": parsed["fields"]["project_id"],
                                    "team_id": parsed["fields"].get("team_id", "")
                                }
                            }
                            response.tool_calls = [corrected_tool_call]
                            return {"messages": [response], "retry_count": retry_count}
                except json.JSONDecodeError:
                    logger.warning("Failed to parse response as JSON")

                # Retry if invalid
                return {
                    "messages": [response],
                    "retry_count": retry_count + 1
                }

            return {"messages": [response], "retry_count": retry_count}

        graph_builder = StateGraph(State)
        graph_builder.add_node("agent", agent)
        graph_builder.add_node("tools", ToolNode(mcp_tools))

        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges(
            "agent",
            tools_condition,
            {
                "tools": "tools",
                END: END,
            }
        )
        graph_builder.add_edge("tools", "agent")

        graph = graph_builder.compile(checkpointer=MemorySaver())
        graph.name = "Email and Linear Agent"

        yield graph
'''
# --------- Connecting to Notion Application --------
# import requests
# headers = {
#     "Authorization": f"Bearer {NOTION_API_TOKEN}",
#     "Content-Type": "application/json",
#     "Notion-Version": "2022-06-28"
# }
# payload = {
#     "parent": {"page_id": "1ea82f3b3e98803689a9e5cfc7caac38"},
#     "properties": {"title": {"title": [{"text": {"content": "Test"}}]}}
# }
# response = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)
# print(response.json())

'''
from contextlib import asynccontextmanager
from typing import Annotated, Sequence, TypedDict
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import BaseMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
import logging
import asyncio
from anyio import ClosedResourceError
import json
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    retry_count: int

@asynccontextmanager
async def make_graph():
    system_prompt = (
        "You are an assistant that uses three tools: `send_email`, `create_linear_issue`, and `create_notion_page`. "
        "For email-related queries, invoke `send_email` with parameters: `recipient` (string), `subject` (string), `body` (string). "
        "For Linear-related queries (e.g., creating tasks or issues), invoke `create_linear_issue` with parameters: `title` (string), `description` (string), `project_id` (string), `team_id` (string). "
        "The `team_id` is REQUIRED for creating Linear issues. For example: "
        "`create_linear_issue(title='Sample Task', description='This is a test issue.', project_id='9d542fc5-44d8-45cb-8a59-fda8f503ed79', team_id='your_team_id')`. "
        "For Notion-related queries (e.g., creating pages), invoke `create_notion_page` with parameters: `title` (string), `content` (string), `parent_page_id` (string). "
        "For example: `create_notion_page(title='Sample Page', content='This is a test page.', parent_page_id='your_parent_page_id')`. "
        "If the query provides `title`, `description`, and `project_id` but omits `team_id` for Linear, respond with: 'Please provide the team ID to create the Linear issue.' "
        "If the query provides `title` and `content` but omits `parent_page_id` for Notion, respond with: 'Please provide the parent page ID to create the Notion page.' "
        "If a GraphQL error indicates 'Field \"teamId\" of required type \"String!\" was not provided' for Linear, prompt for `team_id`. "
        "If a Notion API error indicates an invalid `parent_page_id` or authentication issue, prompt for a valid `parent_page_id` or check the API token. "
        "DO NOT wrap parameters in a `fields` object or JSON structure like `{'fields': {...}}`. "
        "DO NOT claim an issue or page was created unless the API confirms success. "
        "DO NOT suggest or generate code using `smtplib`, other libraries, or alternative methods. "
        "Retry up to 3 times if an error occurs. If retries fail, return a clear error message. "
        "If the query doesn't require a tool, respond directly with a concise answer."
    )
    llm = ChatOllama(model="llama3.2:3b", temperature=0, system=system_prompt)

    mcp_client = MultiServerMCPClient({
        "gmail": {
            "command": "python",
            "args": ["app/mcp_servers/gmail_server.py"],
            "transport": "stdio",
        },
        "linear": {
            "command": "python",
            "args": ["app/mcp_servers/linear_server.py"],
            "transport": "stdio",
        },
        "notion": {
            "command": "python",
            "args": ["app/mcp_servers/notion_server.py"],
            "transport": "stdio",
        }
    })

    async with mcp_client:
        mcp_tools = mcp_client.get_tools()
        logger.info(f"Available tools: {[tool.name for tool in mcp_tools]}")
        llm_with_tools = llm.bind_tools(mcp_tools)

        async def agent(state: State):
            logger.info(f"Processing messages: {[msg.content for msg in state['messages']]}, Retry count: {state.get('retry_count', 0)}")
            messages = state["messages"]
            retry_count = state.get("retry_count", 0)

            if retry_count >= 3:
                logger.error("Max retries exceeded for tool call")
                return {
                    "messages": [AIMessage(content="Unable to process request with tools. Please try again or provide the required parameters (e.g., team ID for Linear or parent page ID for Notion).")],
                    "retry_count": retry_count
                }

            response = await llm_with_tools.ainvoke(messages)
            logger.info(f"LLM response: {response}")

            # Check for invalid response (no tool calls, smtplib mention, or specific errors)
            if response.content and ("smtplib" in response.content.lower() or not response.tool_calls):
                logger.warning(f"LLM generated invalid response: {response.content}")

                # Check for missing teamId for Linear
                if "teamId" in response.content.lower() or any("Field \"teamId\" of required type \"String!\" was not provided" in msg.content for msg in messages):
                    logger.info("Detected missing teamId for Linear")
                    return {
                        "messages": [AIMessage(content="Please provide the team ID to create the Linear issue.")],
                        "retry_count": retry_count
                    }

                # Check for missing parent_page_id or Notion API errors
                if "parent_page_id" in response.content.lower() or any("parent.page_id" in msg.content.lower() or "authentication" in msg.content.lower() for msg in messages):
                    logger.info("Detected missing or invalid parent_page_id for Notion")
                    return {
                        "messages": [AIMessage(content="Please provide a valid parent page ID to create the Notion page.")],
                        "retry_count": retry_count
                    }

                # Attempt to parse malformed JSON-like response
                try:
                    if "fields" in response.content:
                        parsed = json.loads(response.content)
                        if "fields" in parsed:
                            fields = parsed["fields"]
                            if all(key in fields for key in ["title", "description", "project_id"]):
                                logger.info("Correcting malformed fields object to Linear tool call")
                                corrected_tool_call = {
                                    "name": "create_linear_issue",
                                    "args": {
                                        "title": fields["title"],
                                        "description": fields["description"],
                                        "project_id": fields["project_id"],
                                        "team_id": fields.get("team_id", "")
                                    }
                                }
                                response.tool_calls = [corrected_tool_call]
                                return {"messages": [response], "retry_count": retry_count}
                            elif all(key in fields for key in ["title", "content", "parent_page_id"]):
                                logger.info("Correcting malformed fields object to Notion tool call")
                                corrected_tool_call = {
                                    "name": "create_notion_page",
                                    "args": {
                                        "title": fields["title"],
                                        "content": fields["content"],
                                        "parent_page_id": fields["parent_page_id"]
                                    }
                                }
                                response.tool_calls = [corrected_tool_call]
                                return {"messages": [response], "retry_count": retry_count}
                except json.JSONDecodeError:
                    logger.warning("Failed to parse response as JSON")

                # Retry if invalid
                return {
                    "messages": [response],
                    "retry_count": retry_count + 1
                }

            return {"messages": [response], "retry_count": retry_count}

        graph_builder = StateGraph(State)
        graph_builder.add_node("agent", agent)
        graph_builder.add_node("tools", ToolNode(mcp_tools))

        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges(
            "agent",
            tools_condition,
            {
                "tools": "tools",
                END: END,
            }
        )
        graph_builder.add_edge("tools", "agent")

        graph = graph_builder.compile(checkpointer=MemorySaver())
        graph.name = "Email, Linear, and Notion Agent"

        yield graph
'''

# ------- Connecting to Slack and Search Documents on Notion ----------

from contextlib import asynccontextmanager
from typing import Annotated, Sequence, TypedDict
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import BaseMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
import logging
import asyncio
from anyio import ClosedResourceError
import json
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    retry_count: int

@asynccontextmanager
async def make_graph():
    system_prompt = (
        "You are an assistant that uses five tools: `send_email`, `create_linear_issue`, `create_notion_page`, `search_notion_documents`, and `post_slack_message`. "
        "For email-related queries, invoke `send_email` with parameters: `recipient` (string), `subject` (string), `body` (string). "
        "For Linear-related queries, invoke `create_linear_issue` with parameters: `title` (string), `description` (string), `project_id` (string), `team_id` (string). "
        "The `team_id` is REQUIRED for Linear issues. Example: "
        "`create_linear_issue(title='Sample Task', description='This is a test issue.', project_id='9d542fc5-44d8-45cb-8a59-fda8f503ed79', team_id='your_team_id')`. "
        "For Notion page creation, invoke `create_notion_page` with parameters: `title` (string), `content` (string), `parent_page_id` (string). "
        "Example: `create_notion_page(title='Sample Page', content='This is a test page.', parent_page_id='your_parent_page_id')`. "
        "For Notion search, invoke `search_notion_documents` with parameter: `query` (string). "
        "Example: `search_notion_documents(query='project plan')`. "
        "For Slack messaging, invoke `post_slack_message` with parameters: `channel` (string, channel ID or name), `message` (string). "
        "Example: `post_slack_message(channel='#general', message='Hello team!')`. "
        "If required parameters are missing (e.g., `team_id` for Linear, `parent_page_id` for Notion, `channel` for Slack), prompt for them. "
        "If a GraphQL error indicates 'Field \"teamId\" of required type \"String!\" was not provided' for Linear, prompt for `team_id`. "
        "If a Notion API error indicates '401 Client Error: Unauthorized', respond with: 'Invalid Notion API token. Please check your NOTION_API_TOKEN.' "
        "If a Slack API error indicates 'invalid_auth' or 'not_authed', respond with: 'Invalid Slack Bot Token. Please check your SLACK_BOT_TOKEN.' "
        "When retrying tools, ALWAYS include all required parameters from the original query. "
        "DO NOT wrap parameters in a `fields` object or JSON structure like `{'fields': {...}}`. "
        "DO NOT claim an action succeeded unless the API confirms success. "
        "DO NOT suggest or generate code using `smtplib`, other libraries, or alternative methods. "
        "Retry up to 3 times if an error occurs. If retries fail, return a clear error message. "
        "If the query doesn't require a tool, respond directly with a concise answer."
    )
    llm = ChatOllama(model="llama3.2:3b", temperature=0, system=system_prompt)

    mcp_client = MultiServerMCPClient({
        "gmail": {
            "command": "python",
            "args": ["app/mcp_servers/gmail_server.py"],
            "transport": "stdio",
        },
        "linear": {
            "command": "python",
            "args": ["app/mcp_servers/linear_server.py"],
            "transport": "stdio",
        },
        "notion": {
            "command": "python",
            "args": ["app/mcp_servers/notion_server.py"],
            "transport": "stdio",
        },
        "slack": {
            "command": "python",
            "args": ["app/mcp_servers/slack_server.py"],
            "transport": "stdio",
        }
    })

    async with mcp_client:
        mcp_tools = mcp_client.get_tools()
        logger.info(f"Available tools: {[tool.name for tool in mcp_tools]}")
        llm_with_tools = llm.bind_tools(mcp_tools)

        async def agent(state: State):
            logger.info(f"Processing messages: {[msg.content for msg in state['messages']]}, Retry count: {state.get('retry_count', 0)}")
            messages = state["messages"]
            retry_count = state.get("retry_count", 0)

            if retry_count >= 3:
                logger.error("Max retries exceeded for tool call")
                return {
                    "messages": [AIMessage(content="Unable to process request with tools. Please try again or provide the required parameters.")],
                    "retry_count": retry_count
                }

            response = await llm_with_tools.ainvoke(messages)
            logger.info(f"LLM response: {response}")

            if response.content and ("smtplib" in response.content.lower() or not response.tool_calls):
                logger.warning(f"LLM generated invalid response: {response.content}")

                # Check for missing parameters or specific errors
                if "teamId" in response.content.lower() or any("Field \"teamId\" of required type \"String!\" was not provided" in msg.content for msg in messages):
                    logger.info("Detected missing teamId for Linear")
                    return {
                        "messages": [AIMessage(content="Please provide the team ID to create the Linear issue.")],
                        "retry_count": retry_count
                    }
                if "parent_page_id" in response.content.lower() or any("parent_page_id" in msg.content.lower() for msg in messages):
                    logger.info("Detected missing or invalid parent_page_id for Notion")
                    return {
                        "messages": [AIMessage(content="Please provide a valid parent page ID to create the Notion page.")],
                        "retry_count": retry_count
                    }
                if any("401 Client Error: Unauthorized" in msg.content for msg in messages):
                    logger.info("Detected Notion authentication error")
                    return {
                        "messages": [AIMessage(content="Invalid Notion API token. Please check your NOTION_API_TOKEN.")],
                        "retry_count": retry_count
                    }
                if any("invalid_auth" in msg.content or "not_authed" in msg.content for msg in messages):
                    logger.info("Detected Slack authentication error")
                    return {
                        "messages": [AIMessage(content="Invalid Slack Bot Token. Please check your SLACK_BOT_TOKEN.")],
                        "retry_count": retry_count
                    }

                # Parse malformed JSON-like response
                try:
                    if "fields" in response.content:
                        parsed = json.loads(response.content)
                        if "fields" in parsed:
                            fields = parsed["fields"]
                            if all(key in fields for key in ["title", "description", "project_id"]):
                                logger.info("Correcting malformed fields to Linear tool call")
                                corrected_tool_call = {
                                    "name": "create_linear_issue",
                                    "args": {
                                        "title": fields["title"],
                                        "description": fields["description"],
                                        "project_id": fields["project_id"],
                                        "team_id": fields.get("team_id", "")
                                    }
                                }
                                response.tool_calls = [corrected_tool_call]
                                return {"messages": [response], "retry_count": retry_count}
                            elif all(key in fields for key in ["title", "content", "parent_page_id"]):
                                logger.info("Correcting malformed fields to Notion create tool call")
                                corrected_tool_call = {
                                    "name": "create_notion_page",
                                    "args": {
                                        "title": fields["title"],
                                        "content": fields["content"],
                                        "parent_page_id": fields["parent_page_id"]
                                    }
                                }
                                response.tool_calls = [corrected_tool_call]
                                return {"messages": [response], "retry_count": retry_count}
                            elif all(key in fields for key in ["channel", "message"]):
                                logger.info("Correcting malformed fields to Slack tool call")
                                corrected_tool_call = {
                                    "name": "post_slack_message",
                                    "args": {
                                        "channel": fields["channel"],
                                        "message": fields["message"]
                                    }
                                }
                                response.tool_calls = [corrected_tool_call]
                                return {"messages": [response], "retry_count": retry_count}
                except json.JSONDecodeError:
                    logger.warning("Failed to parse response as JSON")

                return {
                    "messages": [response],
                    "retry_count": retry_count + 1
                }

            return {"messages": [response], "retry_count": retry_count}

        graph_builder = StateGraph(State)
        graph_builder.add_node("agent", agent)
        graph_builder.add_node("tools", ToolNode(mcp_tools))

        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges(
            "agent",
            tools_condition,
            {
                "tools": "tools",
                END: END,
            }
        )
        graph_builder.add_edge("tools", "agent")

        graph = graph_builder.compile(checkpointer=MemorySaver())
        graph.name = "Email, Linear, Notion, and Slack Agent"

        yield graph
        
