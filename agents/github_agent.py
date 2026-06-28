from agents.llm_provider import llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from agents.bug_fixing_agent import clean_model_text
from backend.state import State

load_dotenv()  

def github_agent(state: State):
    
    prompt = ChatPromptTemplate.from_messages(
        messages=[
            ('system', """
            Your task is to create medium brief nd precise readme file as markdown file for the given code.
            it should not be too long or detailed. 
            it should not look like AI generated. 
            """),
            
            ('human', """
            optimized code:
            {optimized_code}   #  FIXED: Yahan 'i' laga diya hai taaki niche se match ho sake
            
            project name:
            {project_name}
            
            language:
            {language}
            """)
        ]
    )
    
    chain = prompt | llm | StrOutputParser()
    
    # Ab yahan ka key aur upar prompt ka key 100% match ho gaya hai
    response = chain.invoke(
        {
            "optimized_code": state["code"]["optimized"],
            "project_name": state["metadata"]["project_name"],
            "language": state["metadata"]["language"]
        }
    )
    
    return {
        "output": {
            **state["output"],
            "github_readme_file": response
        }
    }
