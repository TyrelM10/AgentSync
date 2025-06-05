import os
import logging
from fastmcp import FastMCP, Context
import requests
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_API_URL = "https://slack.com/api/chat.postMessage"

mcp = FastMCP("Slack Tools", dependencies=['python-dotenv'])

@mcp.tool()
async def post_slack_message(channel: str, message: str, ctx: Context) -> str:
    """
    Post a message to a Slack channel.
    
    Args:
        channel: The Slack channel ID or name (e.g., 'C12345678' or '#general').
        message: The message text to post.
        ctx: The MCP context for logging and execution.
        
    Returns:
        A string confirming the message was posted.
        
    Raises:
        Exception: If the Slack API call fails.
    """
    logger.info(f"Attempting to post message to Slack channel: {channel}")
    
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "channel": channel,
        "text": message
    }
    
    try:
        response = requests.post(SLACK_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        if not result.get("ok"):
            raise Exception(f"Slack API error: {result.get('error', 'Unknown error')}")
        logger.info(f"Successfully posted message to Slack channel: {channel}")
        return f"Posted message to Slack channel {channel}"
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to post Slack message: {str(e)}")
        raise Exception(f"Error posting Slack message: {str(e)}")

if __name__ == "__main__":
    mcp.run()