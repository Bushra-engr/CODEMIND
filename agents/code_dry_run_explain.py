"""Dry-run and explanation node for the MVP graph."""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from agents.bug_fixing_agent import clean_model_text
from agents.llm_provider import llm
from backend.state import State


def code_dryrun_explainer_agent(state: State) -> dict:
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are a beginner-friendly programming teacher.
                Your job is to explain the final optimized code clearly and in detail.

                Rules:
                - Return only the final explanation.
                - Do not include private reasoning.
                - Do not include hidden thinking.
                - Do not use Markdown code fences.
                - Be detailed but easy to understand.
                - Explain like the reader is learning the concept for the first time.
                                
                """,
            ),
            (
                "human",
                """
                Language: {language}
                Final optimized code:
                {code}

                Create a detailed explanation with these sections:

                1. What this code does
                2. Problem intuition
                3. Step-by-step logic
                4. Important variables and their purpose
                5. Detailed dry run with a small example
                6. Edge cases handled by the code
                7. Time complexity
                8. Space complexity
                9. Beginner-friendly summary
                """,
            ),
        ]
    )
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke(
        {
            "language": state["metadata"]["language"],
            "code": state["code"]["optimized"],
        }
    )
    return {"output": {**state["output"], "explanation": clean_model_text(response)}}


# Backward-compatible alias for callers using the original misspelled name.
code_dryrun_explaniner_agent = code_dryrun_explainer_agent
