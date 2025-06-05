from fastmcp import FastMCP, Context
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

mcp = FastMCP("LinearTools", dependencies=["gql", "aiohttp", "python-dotenv"])

@mcp.tool()
async def create_linear_issue(title: str, description: str, project_id: str, team_id: str, ctx: Context) -> str:
    """Creates an issue in Linear with the specified title, description, and project ID."""
    ctx.info(f"Attempting to create Linear issue with title: {title}")
    try:
        api_key = os.getenv("LINEAR_API_KEY")
        if not api_key:
            error_msg = "LINEAR_API_KEY not found in environment variables"
            ctx.error(error_msg)
            raise ValueError(error_msg)

        # Set up GraphQL client without Bearer prefix
        transport = AIOHTTPTransport(
            url="https://api.linear.app/graphql",
            headers={"Authorization": api_key}
        )
        async with Client(transport=transport, fetch_schema_from_transport=True) as client:
            mutation = gql("""
                mutation IssueCreate($input: IssueCreateInput!) {
                    issueCreate(input: $input) {
                        success
                        issue {
                            id
                            title
                        }
                    }
                }
            """)
            params = {
            "input": {
                "title": title,
                "description": description,
                "projectId": project_id,
                "teamId": team_id
                }
            }
            result = await client.execute(mutation, variable_values=params)
            if result["issueCreate"]["success"]:
                issue_id = result["issueCreate"]["issue"]["id"]
                ctx.info(f"Successfully created Linear issue: {issue_id}")
                return f"Created Linear issue {issue_id} with title: {title}"
            else:
                error_msg = "Failed to create Linear issue"
                ctx.error(error_msg)
                raise RuntimeError(error_msg)
    except Exception as e:
        ctx.error(f"Failed to create Linear issue: {str(e)}")
        raise

def get_project_ids():
    from gql import gql, Client
    from gql.transport.aiohttp import AIOHTTPTransport
    import os
    transport = AIOHTTPTransport(url="https://api.linear.app/graphql", headers={"Authorization": os.getenv('LINEAR_API_KEY')})
    client = Client(transport=transport)
    query = gql("query { projects { nodes { id name } } }")
    result = client.execute(query)
    print(result)

if __name__ == "__main__":
    # get_project_ids()
    logger.info("Starting MCP server with STDIO transport...")
    mcp.run()