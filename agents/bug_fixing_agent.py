"""Bug-fixing node for the MVP graph."""

import re

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from agents.llm_provider import llm
from backend.state import State


def clean_model_text(text: str) -> str:
    """Remove reasoning blocks, chatty prefixes, and Markdown code fences."""
    if not text:
        return ""

    text = re.sub(
        r"<(think|reasoning)>.*?</\1>",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    text = text.strip()

    text = re.sub(
        r"^(here('| i)?s|sure|of course|below is|here is).*?:\s*",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    ).strip()

    fence_match = re.search(
        r"```(?:[a-zA-Z0-9_+#.-]+)?\s*\n(.*?)\n```",
        text,
        flags=re.DOTALL,
    )
    if fence_match:
        return fence_match.group(1).strip()

    return text.strip()


def bug_fixing_agent(state: State) -> dict:
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are a code fixing engine.

                Your job is to fix only the actual defects found by the reviewer.

                Rules:
                - Return only the complete corrected source code.
                - Do not explain anything.
                - Do not include reasoning.
                - Do not include analysis.
                - Do not use Markdown.
                - Do not use code fences.
                - Do not optimize unless required to fix the bug.
                - Preserve the original structure, names, comments, and style as much as possible.
                """,
            ),
            (
                "human",
                """
                Language: {language}

                Original code:
                {code}

                Review findings:
                {review_report}

                Return only the complete corrected source code.
                """,
            ),
        ]
    )
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke(
        {
            "language": state["metadata"]["language"],
            "code": state["code"]["original"],
            "review_report": state["analysis"]["review_report"],
        }
    )
    fixed_code = clean_model_text(response)
    if not fixed_code:
        raise ValueError("Bug-fixing agent returned empty code.")
    
    return {"code": {**state["code"], "fixed": fixed_code}}
