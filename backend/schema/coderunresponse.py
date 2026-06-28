from pydantic import BaseModel

class CodeAnalysisResponse(BaseModel):
    analysis_id: str

    success: bool
    message: str

    project_name: str
    code: str
    language: str

    review_report: str
    bugs_found: bool

    fixed_code: str
    optimized_code: str

    github_push: bool

    explanation: str
    documentation: str