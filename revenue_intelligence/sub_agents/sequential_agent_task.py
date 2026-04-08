import os
import dotenv
from google.adk.agents import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent

model = os.getenv("MODEL", "gemini-2.5-flash")

# Create tool for calendar_agent 
def create_calendar_event(
    title: str,
    date: str,
    start_time: str,
    duration_minutes: int,
    description: str
) -> dict:
    """
    Creates a calendar meeting event for the sales team.
    Attendees are pre-configured as the sales team members.

    Args:
        title (str): Meeting title
        date (str): Meeting date in YYYY-MM-DD format
        start_time (str): Start time in HH:MM format (24hr)
        duration_minutes (int): Duration in minutes
        description (str): Meeting agenda and description

    Returns:
        dict: Meeting confirmation with full details
    """

    # Calculate end time
    start_hour, start_min = map(int, start_time.split(":"))
    total_minutes = start_hour * 60 + start_min + duration_minutes
    end_hour = total_minutes // 60
    end_min = total_minutes % 60
    end_time = f"{end_hour:02d}:{end_min:02d}"

    return {
        "status": "success",
        "meeting_title": title,
        "date": date,
        "start_time": start_time,
        "end_time": end_time,
        "duration_minutes": duration_minutes,
        "description": description,
        "meeting_id": f"MTG-{date.replace('-', '')}-001",
        "confirmation": f"✅ Meeting '{title}' scheduled on {date} from {start_time} to {end_time}"
    } 

# Calender Agent
calendar_agent = LlmAgent(
    name="calendar_agent",
    model=model,
    description="Schedules team meetings and creates calendar events for sales reviews.",
    instruction="""
    You are calendar_agent, a scheduling specialist. Your primary goal is to call the create_calendar_event tool with complete data.

    Scope:
    - Schedule a meeting in the user's calendar.
    - Return only calendar-related confirmation.
    - Keep the meeting/event description short and practical.

   Step 1: Data Gathering & Synthesis
    - Title: Use the user's request to create a clear title.
    - Date & Time: Extract from the user's request.
    - Duration: Use user input or default to 60 minutes.
    - Meeting Description: 
        - Look at the conversation history. 
        - Write a 1-2 sentence summary of the context (e.g., 'Discussion regarding the recent Q1 conversion rate analysis').
        - If no context exists, use: 'Team meeting to discuss [Title]'.

    Step 2: Tool Execution
    - You MUST call create_calendar_event using the gathered data. 
    - Do NOT leave the description field empty.

    Step 3: User Confirmation
    - After the tool executes, provide a brief confirmation in this EXACT format:
      Title: [Meeting Title]
      Date: [Date]
      Start time: [Time]
      Duration: [Duration] minutes
      Meeting description: [Generated Description]

    Strict boundaries:
    - Do NOT include business analysis or broad summaries in your response; only the confirmation.
    - Do NOT act as a communication or email agent.
    """,
    tools=[create_calendar_event]
)

# Creat tool for gmail_agent 
TEAM_EMAIL_1 = os.getenv("TEAM_EMAIL_1")
TEAM_EMAIL_2 = os.getenv("TEAM_EMAIL_2")

def send_email(subject: str, body: str) -> dict:
    """
    Sends a summary email to the sales team.
    Recipients are pre-configured as the sales team members.

    Args:
        subject (str): Email subject line
        body (str): Email body content with analysis summary

    Returns:
        dict: Confirmation with email details
    """
    recipients = [TEAM_EMAIL_1, TEAM_EMAIL_2]

    return {
        "status": "success",
        "message": f"Email successfully sent to sales team",
        "recipients": recipients,
        "subject": subject,
        "body_preview": body[:200] + "..." if len(body) > 200 else body,
        "sent_at": "2026-04-07T10:00:00",
        "confirmation": f"✅ Summary email delivered to {', '.join(recipients)}"
    }

# Gmail Agent 
gmail_agent = LlmAgent(
    name="gmail_agent",
    model=model,
    description="Sends summary emails with sales analysis and meeting details to the sales team.",
    instruction="""
    You are a professional communication agent. Your goal is to draft a high-quality email.

    Step 1: Draft the Content
    You MUST summarize the analysis findings provided in the conversation history. Based on that create:
     - Subject: Create a professional subject line.
     - Email Body: Write a detailed email body:
        - In the body, summarize:
            - Include a 'Key Findings' section with 3-4 short bullet points.
     - Meeting Details: After the meeting is scheduled (look at the calendar_agent's output), you MUST include the Title, Date, and Time in a 'Meeting Details' section.

    Step 2: Execute the Tool
    - Pass your drafted subject and the FULL detailed body to the send_email tool.
    - Do NOT call the tool with a blank or generic body.

    Step 3: User Confirmation
    - After the tool executes, provide a brief confirmation in this EXACT format:
        Subject: [Subject]
        Recipients: [Recipients]]
        Analysis Summary: [Email Body]
        Meeting Details: [Meeting Details]

  """, 
    tools=[send_email]
)   

# Sequential Agent 
sequential_agent_task = SequentialAgent(
    name="calendar_gmail_sequential_agent",
    description="Coordinates meeting scheduling and email communication by sequentially invoking calendar_agent and gmail_agent.",
    sub_agents=[calendar_agent, gmail_agent]
) 

