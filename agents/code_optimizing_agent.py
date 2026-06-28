"""Code optimization node for the MVP graph."""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from agents.bug_fixing_agent import clean_model_text
from agents.llm_provider import llm
from backend.state import State


def code_optimizing_agent(state: State) -> dict:
    source_code = state["code"]["fixed"] or state["code"]["original"]

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are a conservative code optimizer.

                Your job is to improve the code only where clearly useful.

                Rules:
                - Return only the complete optimized source code.
                - Do not explain anything.
                - Do not include reasoning.
                - Do not include analysis.
                - Do not use Markdown.
                - Do not use code fences.
                - Keep the solution simple.
                - Do not over-engineer.
                - Do not add unnecessary abstractions.
                - Preserve the original functionality.
                - Preserve comments whenever possible.
                - Improve readability only if it does not make the code more complex.
                - Improve performance only when it is clearly beneficial.
                """
            ),
            (
                "human",
                """
                Language: {language}

                Code:
                {code}

                Return only the complete optimized source code.
                """
            )
        ]
    )

    chain = prompt | llm | StrOutputParser()

    response = chain.invoke(
        {
            "language": state["metadata"]["language"],
            "code": source_code,
        }
    )

    optimized_code = clean_model_text(response)

    if not optimized_code.strip():
        raise ValueError("Optimization agent returned empty code.")

    return {"code": {**state["code"], "optimized": optimized_code}}
