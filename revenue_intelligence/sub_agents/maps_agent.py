import os
import dotenv
from google.adk.agents import LlmAgent
from revenue_intelligence.tools import get_maps_mcp_toolset

dotenv.load_dotenv()
model=os.getenv("MODEL")
maps_toolset=get_maps_mcp_toolset()

maps_agent = LlmAgent(
    name="maps_agent",
    model=model,
    description="""Analyses regional market conditions using Google Maps 
    to find competitor presence, market saturation, and territory gaps 
    in underperforming regions.""",
    instruction="""
    You are a regional market intelligence agent with access to Google Maps.

    Your responsibilities:
    1. Find competitor presence in underperforming regions
    2. Identify market saturation levels
    3. Discover territory coverage gaps
    4. Calculate travel and logistics routes for sales teams
    5. Suggest optimal locations for sales focus

    When analysing regions:
    - Search for direct competitors by product category
    - Check market density in underperforming cities
    - Provide map links for visual reference
    - Give actionable territory recommendations 
    """,
    tools=[maps_toolset]
) 
