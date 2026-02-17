from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json
from tradingagents.agents.utils.agent_utils import get_news, get_global_news, get_macro_summary
from tradingagents.dataflows.config import get_config


def create_news_analyst(llm):
    def news_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]

        tools = [
            get_news,
            get_global_news,
            get_macro_summary,
        ]

        system_message = (
            "You are a news researcher tasked with analyzing recent news and trends over the past week. "
            "Your analysis should integrate both company-specific news and broader macroeconomic context.\n\n"
            
            "IMPORTANT: Start by using get_macro_summary to understand the current economic environment, "
            "then analyze how company-specific news fits into this broader context.\n\n"
            
            "Key Analysis Areas:\n"
            "1. Company-Specific News: Use get_news() for targeted company news\n"
            "2. Global Market Context: Use get_global_news() for broader market trends\n"
            "3. Macro Economic Environment: Use get_macro_summary() to understand:\n"
            "   - Current economic regime (recession, expansion, etc.)\n"
            "   - Interest rate environment\n"
            "   - Inflation trends\n"
            "   - Employment situation\n\n"
            
            "Connect the Dots:\n"
            "- How does the macro environment affect this company's sector?\n"
            "- Is this a cyclical or defensive stock?\n"
            "- Are current news events amplified or dampened by macro conditions?\n"
            "- Example: 'Weak earnings' is more concerning in a recession than in expansion\n\n"
            
            "Provide detailed and fine-grained analysis. Do not simply state trends are mixed."
            + """ Make sure to append a Markdown table at the end of the report to organize key points in the report, organized and easy to read."""
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful AI assistant, collaborating with other assistants."
                    " Use the provided tools to progress towards answering the question."
                    " If you are unable to fully answer, that's OK; another assistant with different tools"
                    " will help where you left off. Execute what you can to make progress."
                    " If you or any other assistant has the FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL** or deliverable,"
                    " prefix your response with FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL** so the team knows to stop."
                    " You have access to the following tools: {tool_names}.\n{system_message}"
                    "For your reference, the current date is {current_date}. We are looking at the company {ticker}",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        prompt = prompt.partial(system_message=system_message)
        prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
        prompt = prompt.partial(current_date=current_date)
        prompt = prompt.partial(ticker=ticker)

        chain = prompt | llm.bind_tools(tools)
        result = chain.invoke(state["messages"])

        report = ""

        if len(result.tool_calls) == 0:
            report = result.content

        return {
            "messages": [result],
            "news_report": report,
        }

    return news_analyst_node
