from langchain.output_parsers import ResponseSchema, StructuredOutputParser # type: ignore
from services.read_resume import read_resume # type: ignore
from utils.json_extractor import extract_json_block 
from core.llm_engine import generate_text 
def extract_skills_for_cv(cv_path):
    cv_text=read_resume(cv_path)
    skills_schema = ResponseSchema(
    name="skills",
    description="""
Structured list of skills categorized as follows:
- programming_languages: individual programming languages
- frameworks_and_libraries: software frameworks or libraries
- tools_and_platforms: tools, IDEs, platforms, or services
- domain_knowledge: professional or domain-specific knowledge areas
- technical_concepts: technical concepts or methodologies
- soft_skills: interpersonal or soft skills
Return empty lists if a category is not mentioned.
"""
)
    
    cv_schema=[skills_schema]
    output_parser=StructuredOutputParser.from_response_schemas(cv_schema)
    format_instructions=output_parser.get_format_instructions()


    cv_prompt = f"""
    Extract skills from the CV below and return ONLY valid JSON with the following format:
    
    {{
      "skills": {{
        "programming_languages": [],
        "frameworks_and_libraries": [],
        "tools_and_platforms": [],
        "domain_knowledge": [],
        "technical_concepts": [],
        "soft_skills": []
      }}
    }}
    
    - Do NOT include explanations, comments, or code blocks.
    - If a category is empty, keep it as an empty list.
    - Fill the lists only with skills explicitly mentioned in the CV.
    {format_instructions}
    
    CV TEXT:
    {cv_text}
    """




    
    cv_response=generate_text(cv_prompt,max_new_tokens=700)[0]
    cv_json=extract_json_block(cv_response)
    cv_output = output_parser.parse(cv_json)
    return cv_output

