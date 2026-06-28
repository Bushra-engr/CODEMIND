"""Code review node for the MVP graph."""

from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

from agents.llm_provider import llm
from backend.state import State


class ReviewOutput(BaseModel):
    review_report: str = Field(description="Concise code review report")
    bugs_found: bool = Field(description="True if code has actual bugs")


def code_reviewer_agent(state: State) -> dict:
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are a senior software code reviewer.

Review the code for:
- syntax errors
- runtime errors
- logical bugs
- edge case issues
- security issues
- important performance issues
- code smells

Rules:
- Do not fix the code.
- Do not optimize the code.
- Do not rewrite the code.
- Be concise and useful.
- Set bugs_found true only if there is an actual bug that needs fixing.
- Return only valid JSON.

JSON format:
{{
  "review_report": "your review here",
  "bugs_found": true
}}
""",
            ),
            (
                "human",
                """
Language: {language}

Code:
{code}

Review this code and return only the JSON result.
""",
            ),
        ]
    )

    chain = prompt | llm.with_structured_output(
        ReviewOutput,
        method="json_mode",
    )

    response = chain.invoke(
        {
            "language": state["metadata"]["language"],
            "code": state["code"]["original"],
        }
    )

    return {
        "analysis": {
            "review_report": response.review_report,
            "bugs_found": response.bugs_found,
        }
    }