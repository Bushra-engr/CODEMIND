from pydantic import BaseModel, field_validator

class GitHubPushRequest(BaseModel):
    analysis_id: str  # Code body text bypass karke direct analysis row target mapping
    repo_name: str
    is_private: bool

    @field_validator("repo_name")
    def validate_repo_name(cls, value):
        if " " in value:
            raise ValueError("Repository name cannot contain spaces. Use hyphens (-) instead.")
        return value
