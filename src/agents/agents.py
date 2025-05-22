from langgraph.prebuilt import create_react_agent

from src.prompts import apply_prompt_template
from src.tools import (
    bash_tool,
    browser_tool,
    crawl_tool,
    python_repl_tool,
    tavily_tool,
)

from src.llms.llm import get_llm_by_type
from src.config.agents import AGENT_LLM_MAP

# Use Ghostcoder
sys.path.append(os.path.abspath('../../../BIA-Ghostcoder/'))
from ghostcoder.graph import create_ghostcoder_agent


# Create agents using configured LLM types
def create_agent(agent_type: str, tools: list, prompt_template: str):
    """Factory function to create agents with consistent configuration."""
    return create_react_agent(
        get_llm_by_type(AGENT_LLM_MAP[agent_type]),
        tools=tools,
        prompt=lambda state: apply_prompt_template(prompt_template, state),
    )


# Create agents using the factory function
research_agent = create_agent("researcher", [tavily_tool, crawl_tool], "researcher")
coder_agent = create_agent("coder", [python_repl_tool, bash_tool], "coder")
browser_agent = create_agent("browser", [browser_tool], "browser")

ghostcoder_agent = create_ghostcoder_agent(
    chat_model = get_llm_by_type(AGENT_LLM_MAP["planner"]), # Reasoning model
    code_model = get_llm_by_type(AGENT_LLM_MAP["coder"]), # Basic model
    name = "GhostCoder",
    max_retry = 3,
)