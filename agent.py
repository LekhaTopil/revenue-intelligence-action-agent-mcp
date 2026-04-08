import os 
import dotenv
from google.adk.agents import LlmAgent
from revenue_intelligence.sub_agents import (
    analysis_agent, 
    maps_agent,
    sequential_agent_task
)
  
dotenv.load_dotenv() 
model=os.getenv("MODEL", "gemini-2.5-flash")

root_agent = LlmAgent(
    name="corporate_revenue_orchestrator",
    model=model,
    description="""Primary orchestrator for corporate revenue intelligence. 
    Coordinates analysis, regional intelligence, scheduling, 
    and communications to complete end-to-end workflows.""",
    instruction="""
    You are the primary orchestrator for a Corporate Revenue Intelligence System. 
    Your goal is to delegate user requests to the correct specialist sub-agent.

    You coordinate 3 specialist sub-agents:

    1. analysis_agent — Use for any sales data analysis, conversion questions,
       performance comparisons, root cause identification

    2. maps_agent — Use for regional market intelligence, competitor analysis,
       territory gaps, location-based insights

   3. sequential_agent_task: Use for combined requests involving BOTH scheduling meeting (Calendar) and communication (Gmail).

    Workflow Rules:
      - For analysis questions → always use analysis_agent first
      - For regional questions → use maps_agent 
      - For ANY request involving scheduling meeting, emails, or both → Delegate to sequential_agent_task.
    
    Example workflows:

      1. "Why is Q1 conversion low?"
          → Call analysis_agent.

      2. "Which region is underperforming? Find competitors there."
         → Call maps_agent.
         → Use current conversation context if the underperforming region is already available.
         → If the region is not available in the current context, ask the user to clarify which region to search.

      3. "Schedule a meeting and send the update to the team."
         → The user is asking for both scheduling and communication.
         → Check whether the required summary, analysis, or report already exists in the current context.
         → If available, call sequential_agent_task.
         → If not available, ask the user what update or summary should be included before proceeding.

    Always provide a complete, structured response from the relevant sub-agents.
    """,
    sub_agents=[
        analysis_agent,
        maps_agent,
        sequential_agent_task
    ]
) 

