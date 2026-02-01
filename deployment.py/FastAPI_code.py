from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import nest_asyncio
import uvicorn
import pandas as pd
import numpy as np
from models.cv_schema import extract_skills_for_cv
from models.job_description_schema import extract_skills_for_jd
from core.llm_engine import generate_text
from services.read_jobDescription import read_job_description
from services.read_resume import read_resume
from utils.constants import KNOWN_SKILL_WORDS
from utils.json_extractor import extract_json_block
from utils.text_utils import (flatten_skills, skill_match_status, normalize_skill, normalize_skills_output, smart_split, ensure_skills_dict, build_matching_table, build_matching_report,calculate_score,matching_to_dataframe,prettify_matching_df,calculate_match_score,generate_recommendation,generate_summary_df)


nest_asyncio.apply()
app = FastAPI()


def convert_numpy(obj):
    """تحويل أنواع numpy لأنواع JSON-friendly"""
    if isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy(i) for i in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return [convert_numpy(i) for i in obj]
    else:
        return obj

def convert_report(report):
    """تحويل الـ DataFrame و numpy objects لأي JSON-friendly structure"""
    if isinstance(report, pd.DataFrame):
        # تحويل الـ DataFrame لقائمة dicts
        return [convert_numpy(row) for row in report.to_dict(orient="records")]
    elif isinstance(report, list):
        return [convert_report(item) for item in report]
    elif isinstance(report, dict):
        return {k: convert_report(v) for k, v in report.items()}
    else:
        return convert_numpy(report)

# =======================
# الـ endpoint
# =======================
@app.post("/analyze")
async def analyze(cv_file: UploadFile = File(...), job_description: str = Form(...)):
    
    temp_path = f"/tmp/{cv_file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await cv_file.read())

    # تحليل الـ CV والـ JD
    cv_skills = extract_skills_for_cv(temp_path)
    jd_skills = extract_skills_for_jd(job_description)
    matching_results = build_matching_table(jd_skills, cv_skills)
    report = build_matching_report(matching_results)

    # تحويل كل شيء لـ JSON-friendly
    
    report_json = convert_report(report)
    report_json["__debug_cv_skills"] = cv_skills
    report_json["__debug_jd_skills"] = jd_skills
    return JSONResponse(content=report_json)

# =======================
# تشغيل السيرفر
# =======================
import threading

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8001)

thread = threading.Thread(target=run_server, daemon=True)
thread.start()
print("FastAPI server is running in background!")

