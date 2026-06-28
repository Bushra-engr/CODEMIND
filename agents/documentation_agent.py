from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from agents.bug_fixing_agent import clean_model_text
from agents.llm_provider import llm
from backend.state import State


def documentation_agent(state: State) -> dict:
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are a technical documentation writer.

            Your job is to create clear developer documentation from the final optimized code.

            Rules:
            - Return only final Markdown documentation.
            - Do not include private reasoning.
            - Do not include hidden thinking.
            - Do not wrap the whole response in Markdown code fences.
            - Use only the supplied code.
            - Be detailed enough that another developer can understand, run, and maintain the code.
            """
        ),
        (
            "human",
            """
            Project name: {project_name}
            Language: {language}

            Final optimized code:
            {optimized_code}

            Create detailed Markdown documentation with these sections:

            # {project_name}

            ## Overview

            ## Problem Statement

            ## Approach / Algorithm

            ## How the Code Works

            ## Main Functions / Classes / Variables

            ## Input Format

            ## Output Format

            ## Example Usage

            ## Dry Run

            ## Time Complexity

            ## Space Complexity

            ## Assumptions

            ## Notes for Developers
"""
        ),
    ])

    response = (prompt | llm | StrOutputParser()).invoke({
        "project_name": state["metadata"]["project_name"],
        "language": state["metadata"]["language"],
        "optimized_code": state["code"]["optimized"],
    })

    return {
        "output": {
            **state["output"],
            "documentation": response,
        }
    }
