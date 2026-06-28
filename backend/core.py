
from __future__ import annotations

from pathlib import Path
from typing import Any
from uuid import uuid4

from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from agents.documentation_agent import documentation_agent
from agents.bug_fixing_agent import bug_fixing_agent
from agents.code_dry_run_explain import code_dryrun_explainer_agent
from agents.code_optimizing_agent import code_optimizing_agent
from agents.code_reviewer_agent import code_reviewer_agent
from agents.github_agent import github_agent
from backend.state import State, create_initial_state

load_dotenv()


def _review_route(state: State) -> str:
    """Route reviewed code to fixing only when the reviewer found bugs."""
    return "bugs_found" if state["analysis"]["bugs_found"] else "no_bugs"

def github_router(state:State):
    if state['metadata']["github_push"] == True:
        return "yes"
    else:
        return "no"

def build_graph(checkpointer: Any | None = None):
    """Build and compile the MVP reviewer -> fixer -> optimizer workflow."""
    builder = StateGraph(State)
    builder.add_node("review", code_reviewer_agent)
    builder.add_node("fix", bug_fixing_agent)
    builder.add_node("optimize", code_optimizing_agent)
    builder.add_node("explain", code_dryrun_explainer_agent)
    builder.add_node("documentation",documentation_agent)
    builder.add_node("github",github_agent)
    
    builder.add_edge(START, "review")
    builder.add_conditional_edges(
        "review",
        _review_route,
        {"bugs_found": "fix", "no_bugs": "optimize"},
    )
    builder.add_edge("fix", "optimize")
    builder.add_edge("optimize", "explain")
    builder.add_edge("explain", "documentation")
    builder.add_conditional_edges("documentation",github_router,{
        "yes":"github",
        "no":END
    })
    builder.add_edge("github", END)
    return builder.compile(checkpointer=checkpointer)


# Reuse one compiled graph in the process. Each invocation gets its own thread ID.
graph = build_graph(checkpointer=InMemorySaver())


def run_assistant(
    *,
    code: str,
    language: str,
    project_name: str,
    github_push:bool,
    thread_id: str | None = None,
) -> State:
    """Run the MVP workflow and return its complete final state."""
    if not code.strip():
        raise ValueError("Code cannot be empty.")
    if not language.strip():
        raise ValueError("Language cannot be empty.")
    if not project_name.strip():
        raise ValueError("Project name cannot be empty.")

    config = {"configurable": {"thread_id": thread_id or str(uuid4())}}
    return graph.invoke(
        create_initial_state(
            code=code,
            language=language.strip(),
            project_name=project_name.strip(),
            github_push=github_push
        ),
        config=config
    )


def main() -> None:
    """Small CLI for manually exercising the MVP."""
    print("=" * 80)
    print("AI POWERED CODING ASSISTANT - MVP")
    print("=" * 80)

    project_name = input("Enter project / code name: ").strip()
    language = input("Enter the code language: ").strip()
    default_file = Path(__file__).with_name("sample_code.txt")
    entered_path = input(f"Enter code file path [{default_file}]: ").strip()
    file_path = Path(entered_path) if entered_path else default_file
    github_push = input("Github push ?(yes/no)")
    if github_push.lower()=="yes":
        github_push = True
    else:
        github_push = False

    try:
        code = file_path.read_text(encoding="utf-8")
        response = run_assistant(
            code=code,
            language=language,
            project_name=project_name,
            github_push = github_push
        )
    except (OSError, UnicodeError, ValueError) as exc:
        raise SystemExit(f"Error: {exc}") from exc

    sections = (
        ("REVIEW REPORT", response["analysis"]["review_report"]),
        ("BUGS FOUND", response["analysis"]["bugs_found"]),
        ("FIXED CODE", response["code"]["fixed"] or "No fixes required."),
        ("OPTIMIZED CODE", response["code"]["optimized"]),
        ("DRY RUN & EXPLANATION", response["output"]["explanation"]),
        ("DOCUMENTATION", response["output"]["documentation"])
    )
    for title, value in sections:
        print(f"\n{'=' * 80}\n{title}\n{value}")


if __name__ == "__main__":
    main()
