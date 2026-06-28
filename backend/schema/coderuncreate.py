from pydantic import BaseModel, Field , field_validator


class CodeRunCreate(BaseModel):
    project_name:str = Field(
        description="name of the code/project",
        min_length=10,
        max_length=100
    )
    code:str = Field(
        description="Code entered by user to analyze",
        min_length=10
    )
    language : str = Field(
        description="language of the code.",
        min_length=2,
        max_length=30
    )
    
    github : bool  = Field(
        description="Do you want to push the code to the github?"
    )
    
    @field_validator("language")
    def validate_lang(cls,value):
        
        allowed = [
        "python",
        "cpp",
        "java",
        "javascript"
    ]
        
        if value.lower() not in allowed:
            raise ValueError("Unsupported Language")
        
        return value
    