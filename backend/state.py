"""Shared state contract for the MVP agent graph."""

from __future__ import annotations

from typing import TypedDict


class MetadataState(TypedDict):
    language: str
    project_name: str
    github_push :bool

class CodeState(TypedDict):
    original: str
    fixed: str
    optimized: str


class AnalysisState(TypedDict):
    review_report: str
    bugs_found: bool


class OutputState(TypedDict):
    explanation: str
    documentation:str
    github_readme_file: str
    

class State(TypedDict):
    metadata: MetadataState
    code: CodeState
    analysis: AnalysisState
    output: OutputState


def create_initial_state(*, code: str, language: str, project_name: str,github_push:bool) -> State:
    """Create one valid state instead of duplicating its nested shape at callers."""
    return {
        "metadata": {"language": language, "project_name": project_name,"github_push":github_push},
        "code": {"original": code, "fixed": "", "optimized": ""},
        "analysis": {"review_report": "", "bugs_found": False},
        "output": {"explanation": "", "documentation": "", "github": ""},
    }
