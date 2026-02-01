# 📄 Resume Analyzer & Job Matching System

An AI-powered system that analyzes resumes (CVs) and job descriptions, extracts structured skills using Large Language Models (LLMs), and computes a matching score with clear, actionable insights.

This project is designed with **clean architecture**, **modular services**, and **production-ready structure**, making it suitable for real-world deployment and academic or professional portfolios.

---

## 📑 Table of Contents

* [Features](#-features)
* [Tech Stack](#-tech-stack)
* [Project Structure](#-project-structure)
* [Installation](#-installation)
* [How to Run Using Streamlit](#-how-to-run-using-streamlit)
* [How It Works](#-how-it-works)
* [API Overview](#-api-overview)
* [Future Improvements](#-future-improvements)

---

## ✨ Features

* 📄 Upload and parse **PDF resumes**
* 📝 Analyze **job descriptions** (text-based)
* 🤖 Skill extraction using **LLMs (Mistral / Transformers)**
* 🧠 Structured skill categorization:

  * Programming Languages
  * Frameworks & Libraries
  * Tools & Platforms
  * Domain Knowledge
  * Technical Concepts
  * Soft Skills
* 📊 Skill matching with:

  * Exact match
  * Partial match
  * Missing skills
* 🎯 Final matching score & decision
* 📋 Human-readable recommendation report
* ⚙️ Modular, scalable project architecture

---

## 🧰 Tech Stack

### Backend

* **FastAPI** – API framework
* **Uvicorn** – ASGI server

### AI & NLP

* **Transformers (HuggingFace)**
* **PyTorch**
* **LangChain**
* **Mistral Instruct Models**

### Data & Parsing

* **PDFPlumber** – PDF text extraction
* **Pandas / NumPy** – Data processing

### Frontend

* **Streamlit** – Interactive UI

---

## 🗂 Project Structure

```bash
resume-analyzer/
│
├── app/
│   └── main.py                  # FastAPI entry point
│
├── core/
│   └── llm_engine.py             # Model loading & text generation
│               
│
├── deployment/
│   ├── FastAPI_code.py           # FastAPI app setup
│   └── ngrok.py                  # ngrok tunnel setup
│
├── models/
│   ├── cv_schema.py              # CV output schema
│   └── job_description_schema.py # JD output schema
│
├── services/
│   ├── read_resume.py            # Resume reading & preprocessing
│   └── read_jobDescription.py    # Job description handling
│
├── utils/
│   ├── constants.py              # Shared constants
│   ├── json_extractor.py         # Robust JSON parsing from LLM output
│   └── text_utils.py             # Text normalization & helpers
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/HebaHossam68/Resume-Analyzer-Job-Matcher-ATS-.git
cd resume-analyzer
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\\Scripts\\activate     # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run Using Streamlit

```bash
streamlit run app/main.py
```

Then open your browser at:

```
http://localhost:8001
```

---

## 🔄 How It Works

1. User uploads a **CV (PDF)** and enters a **Job Description**
2. Text is extracted and cleaned
3. LLM extracts structured skills using strict JSON schema
4. Skills are normalized and compared
5. Matching table and final score are generated
6. Results are displayed via API or Streamlit UI

---

## 🔌 API Overview

### `POST /analyze`

**Inputs:**

* CV file (PDF)
* Job description text

**Response:**

```json
{
  "final_score": 24.0,
  "decision": "Needs Improvement ⚠️",
  "recommendation": "❌ Not a good fit",

  "matching_table": [
    {
      "Skill": "Python",
      "Status": "✅ Match",
      "Action Needed": "No Action Needed"
    },
    {
      "Skill": "Javascript",
      "Status": "✅ Match",
      "Action Needed": "No Action Needed"
    },
    {
      "Skill": "Django",
      "Status": "❌ Missing",
      "Action Needed": "Improve / Learn"
    },
    {
      "Skill": "Flask",
      "Status": "✅ Match",
      "Action Needed": "No Action Needed"
    },
    {
      "Skill": "Restful Apis",
      "Status": "❌ Missing",
      "Action Needed": "Improve / Learn"
    },
    {
      "Skill": "Microservices",
      "Status": "❌ Missing",
      "Action Needed": "Improve / Learn"
    },
    {
      "Skill": "Postgresql",
      "Status": "❌ Missing",
      "Action Needed": "Improve / Learn"
    },
    {
      "Skill": "Mysql",
      "Status": "❌ Missing",
      "Action Needed": "Improve / Learn"
    },
    {
      "Skill": "Aws",
      "Status": "❌ Missing",
      "Action Needed": "Improve / Learn"
    },
    {
      "Skill": "Azure",
      "Status": "🟡 Partial",
      "Action Needed": "Improve / Learn"
    },
    {
      "Skill": "Docker",
      "Status": "❌ Missing",
      "Action Needed": "Improve / Learn"
    },
    {
      "Skill": "Ci/Cd",
      "Status": "❌ Missing",
      "Action Needed": "Improve / Learn"
    },
    {
      "Skill": "Data Structures",
      "Status": "✅ Match",
      "Action Needed": "No Action Needed"
    },
    {
      "Skill": "Problem Solving",
      "Status": "❌ Missing",
      "Action Needed": "Improve / Learn"
    },
    {
      "Skill": "Communication",
      "Status": "❌ Missing",
      "Action Needed": "Improve / Learn"
    },
    {
      "Skill": "Teamwork",
      "Status": "❌ Missing",
      "Action Needed": "Improve / Learn"
    },
    {
      "Skill": "Software Engineering",
      "Status": "✅ Match",
      "Action Needed": "No Action Needed"
    },
    {
      "Skill": "Kubernetes",
      "Status": "❌ Missing",
      "Action Needed": "Improve / Learn"
    },
    {
      "Skill": "Terraform",
      "Status": "❌ Missing",
      "Action Needed": "Improve / Learn"
    },
    {
      "Skill": "Devops",
      "Status": "❌ Missing",
      "Action Needed": "Improve / Learn"
    },
    {
      "Skill": "Container Orchestration",
      "Status": "❌ Missing",
      "Action Needed": "Improve / Learn"
    },
    {
      "Skill": "Iac",
      "Status": "❌ Missing",
      "Action Needed": "Improve / Learn"
    },
    {
      "Skill": "Serverless",
      "Status": "❌ Missing",
      "Action Needed": "Improve / Learn"
    },
    {
      "Skill": "Aws Lambda",
      "Status": "❌ Missing",
      "Action Needed": "Improve / Learn"
    },
    {
      "Skill": "Api Gateway",
      "Status": "🟡 Partial",
      "Action Needed": "Improve / Learn"
    }
  ],

  "summary_table": [
    {
      "Match Type": "Yes",
      "Count": 5
    },
    {
      "Match Type": "Partial",
      "Count": 2
    },
    {
      "Match Type": "No",
      "Count": 18
    }
  ]
}

```

---

## 🚀 Future Improvements

* 🔍 Semantic matching using embeddings (FAISS)
* 📈 Explainable AI insights per missing skill
* 🌐 Cloud deployment (AWS / GCP)
* 🐳 Dockerization
* 🔐 Authentication & user profiles
* 📊 Dashboard analytics

---

## 👩‍💻 Author

**Heba Hossam**
AI & Data Science Engineer | MSc Computer Science

---

⭐ If you find this project helpful, please consider giving it a star on GitHub!
