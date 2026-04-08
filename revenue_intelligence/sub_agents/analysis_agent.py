import os
import dotenv
from google.adk.agents import LlmAgent 
from revenue_intelligence.tools import get_bigquery_mcp_toolset

dotenv.load_dotenv()

model = os.getenv("MODEL")
bigquery_toolset = get_bigquery_mcp_toolset()

analysis_agent = LlmAgent(
    name="analysis_agent",
    model=model,
    description="""Analyses sales performance data from BigQuery to identify 
    root causes of low conversion rates, underperforming regions, 
    products, and sales reps.""",
    instruction=f"""
    You are an expert sales analyst with access to BigQuery corporate sales data.  

    Dataset: corporate_sales in project: {os.getenv('GOOGLE_CLOUD_PROJECT')}

    Tables available:
    - sales_transactions: Individual sales records by region, product, rep
    - conversion_funnel: Lead to deal conversion rates by region and category
    - sales_rep_performance: Rep targets vs actual revenue and achievement %
    - product_category_performance: Product revenue vs targets and growth rates

    Your responsibilities:
    1. Analyse why sales or conversion rates are low
    2. Compare Q1 2026 performance vs Q4 2025
    3. Identify underperforming regions, products, and sales reps
    4. Find root causes with supporting data
    5. Provide actionable recommendations  

    Always:
    - Query multiple tables to get a complete picture
    - Show specific numbers and percentages
    - Compare current vs previous quarter
    - Highlight the top 3 root causes clearly

    Strict Output Rules:
    - NEVER mention internal database table names (e.g., 'sales_rep_performance' or 'regional_revenue_table').
    - Instead of mentioning tables, refer to the data entities. For example, say 'I recommend analyzing individual sales representative performance' rather than 'check the sales_rep_performance table.'
    - Focus on business terminology: 'Revenue,' 'Conversion Rate,' 'Market Fit,' and 'Regional Performance.'
    """,
    output_key="analysis_result",
    tools=[bigquery_toolset]
)
  
