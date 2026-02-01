import re
def extract_json_block(text):
    pattern = r'```json\s*(.*?)\s*```'
    matches = re.findall(pattern, text, re.DOTALL)

    return f"```json\n{matches[-1]}\n```"