from services.read_jobDescription import read_job_description
from langchain.output_parsers import ResponseSchema, StructuredOutputParser # type: ignore
from utils.json_extractor import extract_json_block 
from core.llm_engine import generate_text
def extract_skills_for_jd(jd_text):
    job_description = read_job_description(jd_text)

    skills_schema = ResponseSchema(
        name="skills",
        description="""
A structured object with the following fields:
- programming_languages
- frameworks_and_libraries
- tools_and_platforms
- domain_knowledge
- technical_concepts
- soft_skills

All values must be lists. Use [] if not mentioned.
"""
    )

    output_parser = StructuredOutputParser.from_response_schemas([skills_schema])
    format_instructions = output_parser.get_format_instructions()

    jd_prompt = f"""
    Extract skills from the job description below and return ONLY valid JSON with the following format:
    
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
    
    JD Text:
    {job_description}
    """

    jd_response = generate_text(jd_prompt, max_new_tokens=700)[0]
    jd_json = extract_json_block(jd_response)
    jd_output= output_parser.parse(jd_json)
    return jd_output
