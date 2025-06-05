import os
import json
import logging
from fastmcp import FastMCP, Context
import requests
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

NOTION_API_TOKEN = os.getenv("NOTION_API_TOKEN")

NOTION_API_URL = "https://api.notion.com/v1/pages"
NOTION_SEARCH_URL = "https://api.notion.com/v1/search"
NOTION_API_VERSION = "2022-06-28"

mcp = FastMCP("Notion Tools", dependencies=['python-dotenv'])

@mcp.tool()
async def create_notion_page(title: str, content: str, parent_page_id: str, ctx: Context) -> str:
    """
    Create a page in Notion with the specified title, content, and parent page ID.
    
    Args:
        title: The title of the Notion page.
        content: The content of the Notion page (as a text block).
        parent_page_id: The ID of the parent page in Notion.
        ctx: The MCP context for logging and execution.
        
    Returns:
        A string confirming the page creation with its ID.
        
    Raises:
        Exception: If the Notion API call fails.
    """
    logger.info(f"Attempting to create Notion page with title: {title}")
    # logger.info("THIS IS THE API: ", NOTION_API_TOKEN)
    headers = {
        "Authorization": f"Bearer {NOTION_API_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_API_VERSION
    }
    
    payload = {
        "parent": {"page_id": parent_page_id},
        "properties": {
            "title": {
                "title": [{"text": {"content": title}}]
            }
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": content}}]
                }
            }
        ]
    }
    
    try:
        response = requests.post(NOTION_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        page_id = response.json().get("id")
        logger.info(f"Successfully created Notion page: {page_id}")
        return f"Created Notion page {page_id} with title: {title}"
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to create Notion page: {str(e)}")
        raise Exception(f"Error creating Notion page: {str(e)}")

@mcp.tool()
async def search_notion_documents(query: str, ctx: Context) -> str:
    """
    Search for documents in Notion based on a query string.
    
    Args:
        query: The search term to find Notion pages.
        ctx: The MCP context for logging and execution.
        
    Returns:
        A string listing matching page titles and IDs.
        
    Raises:
        Exception: If the Notion API call fails.
    """
    logger.info(f"Searching Notion documents with query: {query}")
    
    headers = {
        "Authorization": f"Bearer {NOTION_API_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_API_VERSION
    }
    
    payload = {
        "query": query,
        "filter": {"value": "page", "property": "object"}
    }
    
    try:
        response = requests.post(NOTION_SEARCH_URL, headers=headers, json=payload)
        response.raise_for_status()
        results = response.json().get("results", [])
        if not results:
            logger.info("No Notion documents found")
            return "No documents found matching the query."
        pages = [
            f"Title: {r['properties']['title']['title'][0]['text']['content']}, ID: {r['id']}"
            for r in results if r["properties"]["title"]["title"]
        ]
        logger.info(f"Found {len(pages)} Notion documents")
        return "\n".join(pages) or "No documents found with titles."
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to search Notion documents: {str(e)}")
        if "401" in str(e):
            raise Exception("Invalid Notion API token. Please check your NOTION_API_TOKEN.")
        raise Exception(f"Error searching Notion documents: {str(e)}")

if __name__ == "__main__":
    mcp.run()