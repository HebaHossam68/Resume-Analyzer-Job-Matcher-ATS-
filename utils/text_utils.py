import re
from utils.constants import KNOWN_SKILL_WORDS
def smart_split(skill: str) -> str:
    skill = skill.lower().strip()

    # fix common typos
    skill = skill.replace("datastuctures", "data structures")

    # split known words
    for word in KNOWN_SKILL_WORDS:
        skill = re.sub(
            rf"(?<!\s)({word})(?!\s)",
            r" \1 ",
            skill
        )

    # clean extra spaces
    skill = re.sub(r"\s+", " ", skill).strip()
    return skill

def normalize_skills_output(skills_output: dict):
    for category, skills in skills_output["skills"].items():
        skills_output["skills"][category] = sorted(
            set(smart_split(skill) for skill in skills)
        )
    return skills_output

import re

def normalize_skill(skill: str) -> str:
    skill = skill.lower()
    skill = re.sub(r"[^\w\s]", " ", skill)   # remove symbols
    skill = re.sub(r"_", " ", skill)
    skill = re.sub(r"\s+", " ", skill).strip()
    return skill

def flatten_skills(skills_dict):
    all_skills = []
    for category, skills in skills_dict["skills"].items():
        for skill in skills:
            all_skills.append(normalize_skill(skill))
    return set(all_skills)

def skill_match_status(jd_skill, cv_skills):
    jd = normalize_skill(jd_skill)
    jd_tokens = set(jd.split())

    for cv_skill in cv_skills:
        cv = normalize_skill(cv_skill)
        cv_tokens = set(cv.split())

        # exact
        if jd == cv:
            return "Yes", "No"

        # partial
        overlap = jd_tokens & cv_tokens
        if overlap and len(overlap) / len(jd_tokens) >= 0.3:
            return "Partial", "Yes"

    return "No", "Yes"

def build_matching_table(jd_skills, cv_skills):
    table = []

    for category, skills in jd_skills["skills"].items():
        for skill in skills:
            
            present, needs_improvement = skill_match_status(
                skill,          
                cv_skills
            )

            table.append({
                "Skill": skill.title(),
                "Present": present,
                "Needs_Improvement": needs_improvement
            })

    return table

def calculate_score(matching_table):
    score = 0
    max_score = len(matching_table)

    for row in matching_table:
        if row["Present"] == "Yes":
            score += 1
        elif row["Present"] == "Partial":
            score += 0.5

    percentage = round((score / max_score) * 100, 2)

    decision = "Good Fit ✅" if percentage >= 70 else "Needs Improvement ⚠️"

    return percentage, decision

import pandas as pd

def matching_to_dataframe(matching_results):
    df = pd.DataFrame(matching_results)
    return df

def prettify_matching_df(df):
    df = df.copy()

    status_map = {
        "Yes": "✅ Match",
        "Partial": "🟡 Partial Match",
        "No": "❌ Missing"
    }

    df["Status"] = df["Present"].map(status_map)
    df["Action Needed"] = df["Present"].apply(
        lambda x: "No Action Needed" if x == "Yes" else "Improve / Learn"
    )

    df["Skill"] = df["Skill"].str.title()

    return df[["Skill", "Status", "Action Needed"]]

def calculate_match_score(df):
    weights = {
        "Yes": 1.0,
        "Partial": 0.5,
        "No": 0.0
    }

    df["Score"] = df["Present"].map(weights)

    final_score = round(df["Score"].mean() * 100, 2)
    return final_score

def generate_recommendation(match_score):
    if match_score >= 75:
        return "✅ Strong fit for the role"
    elif match_score >= 50:
        return "⚠️ Partial fit – candidate needs skill improvement"
    else:
        return "❌ Not a good fit for this role"
    
def generate_summary_df(df):
    summary = df["Present"].value_counts().reset_index()
    summary.columns = ["Match Type", "Count"]

    summary["Match Type"] = summary["Match Type"].map({
        "Yes": "Matched",
        "Partial": "Partial Match",
        "No": "Missing"
    })

    return summary

def build_matching_report(matching_results):
    raw_df = matching_to_dataframe(matching_results)
    pretty_df = prettify_matching_df(raw_df)
    score = calculate_match_score(raw_df)
    recommendation=generate_recommendation(score)
    summary_df = generate_summary_df(raw_df)

    decision = (
        "Strong Fit 💪" if score >= 80
        else "Good Fit 👍" if score >= 65
        else "Needs Improvement ⚠️"
    )

    return {
        "final_score": score,
        "decision": decision,
        "matching_table": pretty_df,
        "summary_table": summary_df,
        "recommendation":recommendation
    }

def ensure_skills_dict(skills_json: dict):
    empty_structure = {
        "programming_languages": [],
        "frameworks_and_libraries": [],
        "tools_and_platforms": [],
        "domain_knowledge": [],
        "technical_concepts": [],
        "soft_skills": []
    }

    skills = skills_json.get("skills", {})

    # لو skills طالعة list
    if isinstance(skills, list):
        empty_structure["technical_concepts"] = skills
        return {"skills": empty_structure}

    # لو skills dict
    for key in empty_structure:
        empty_structure[key] = skills.get(key, [])

    return {"skills": empty_structure}

