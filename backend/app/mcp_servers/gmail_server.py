from fastmcp import FastMCP, Context
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
import base64
from email.mime.text import MIMEText
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

mcp = FastMCP("GmailTools", dependencies=["google-auth", "google-auth-oauthlib", "google-api-python-client", "python-dotenv"])

@mcp.tool()
def send_email(recipient: str, subject: str, body: str, ctx: Context) -> str:
    """Sends an email via Gmail."""
    ctx.info(f"Attempting to send email to {recipient}")
    try:
        credentials_path = os.getenv("GMAIL_CREDENTIALS_PATH")
        if not credentials_path or not os.path.exists(credentials_path):
            error_msg = f"Credentials file not found at {credentials_path}"
            ctx.error(error_msg)
            raise FileNotFoundError(error_msg)
        
        creds = None
        if os.path.exists("token.json"):
            ctx.info("Loading credentials from token.json")
            creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/gmail.send"])
        
        if not creds or not creds.valid:
            ctx.info("Initiating OAuth flow")
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, ["https://www.googleapis.com/auth/gmail.send"]
            )
            creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                ctx.info("Saving new token to token.json")
                token.write(creds.to_json())
        
        service = build("gmail", "v1", credentials=creds)
        
        message = MIMEText(body)
        message["to"] = recipient
        message["subject"] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        service.users().messages().send(userId="me", body={"raw": raw}).execute()
        ctx.info(f"Email successfully sent to {recipient}")
        return f"Email sent to {recipient}"
    except Exception as e:
        ctx.error(f"Failed to send email: {str(e)}")
        raise

if __name__ == "__main__":
    logger.info("Starting MCP server with STDIO transport...")
    mcp.run()