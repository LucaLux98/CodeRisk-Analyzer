from fastapi import FastAPI         # WEB API IN PYTHON
from fastapi import UploadFile, File    # UPLOAD FILE
from fastapi.responses import Response  # REPORT
import os
import json
from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel      # DEFINITION AND VALIDATION PYTHON DATA

from ai.ai_explainer import generate_ai_insights    # AI
from ai.llm import call_llm

from app.analyzers.basic_analyzer import b_analyze_python_code       # TRIPLE-BASIC CHECKS
from app.analyzers.ast_analyzer import ast_analyze_python_code       # AST CHECKS
from app.analyzers.risk_score import calculate_risk_score            # RISK SCORE

app = FastAPI()     # API "CONTAINER"

class CodeRequest (BaseModel):      # INPUT SCHEME (JSON VALIDATION)
    code: str

REPORT_FOLDER = "REPORT"        # REPORT FOLDER NAME

def save_report(report: dict):      # REPORT SAVING
    os.makedirs(REPORT_FOLDER, exist_ok = True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")        # FILE WITH TIMESTAMP
    filename = f"report_{timestamp}.json"
    path = os.path.join(REPORT_FOLDER, filename)

    with open(path, "w", encoding = "utf-8") as f:
        json.dump(report, f, indent = 4)
    return path

def generate_summary(issues):       # SUMMARY
    if not issues:
        return "No security issues detected."
    
    types = {issue.get("type") for issue in issues}
    if "dangerous function" in types:
        return "Potential code injection risks detected."
    if "hardcoded secret" in types:
        return "Possible password hardcoded."
    if "API Key Exposure" in types:
        return "Token/API key detected."
    if "User Input" in types:
        return "Input detected."
    if "syntax Error" in types:
        return "Syntax Error detected."
    
    return "Security issues detected in code."

def get_risk_level(score: int):     # RISK LEVEL
    if score <= 15:
        return "low"
    elif score <= 49:
        return "medium"
    else:
        return "high"
    
@app.get("/")       # BASIC ENDPOINT
def home ():
    return {"status": "ok"}

@app.post("/analyze")           # ANALYSIS ENDPOINT
def analyze(request: CodeRequest):
    
    code = request.code
    ast_iss = ast_analyze_python_code(code)
    bas_iss = b_analyze_python_code(code)
    tot_iss = ast_iss + bas_iss

    unique_issues = []
    seen = set()
    for issue in tot_iss:
        key = (
            issue.get("type")
        )

        if key not in seen:
            seen.add(key)
            unique_issues.append(issue)

    r_score = calculate_risk_score(unique_issues)
    r_level = get_risk_level(r_score)
    summary = generate_summary(unique_issues)

    return {
        "risk": {
            "score": r_score,
            "level": r_level
        },
        "results": {
            "issues_found": len(unique_issues),
            "issues": unique_issues
        },
        "status": "analyzed",
        "summary": summary
    }

@app.post ("/analyze-file")                 # ENDPOINT ANALYZE FILE
async def analyze_file(file: UploadFile = File(...)):
    code = (await file.read()).decode("utf-8")
    
    ast_iss = ast_analyze_python_code(code)
    bas_iss = b_analyze_python_code(code)
    tot_iss = ast_iss + bas_iss

    unique_issues = []
    seen = set()
    for issue in tot_iss:
        key = (
            issue.get("type")
        )

        if key not in seen:
            seen.add(key)
            unique_issues.append(issue)

    r_score = calculate_risk_score(unique_issues)
    r_level = get_risk_level(r_score)
    summary = generate_summary(unique_issues)

    return {
        "filename": file.filename,
        "status": "analyzed",
        "summary": summary,
        "risk": {
            "score": r_score,
            "level": r_level
        },
        "results": {
            "issues_found": len(unique_issues),
            "issues": unique_issues
        }
    }

@app.post ("/analyze-file-report & AI")          # ENDPOINT ANALYZE FILE WITH INSTANT DOWNLOAD
async def analyze_file(file: UploadFile = File(...)):
    code = (await file.read()).decode("utf-8")
    
    ast_iss = ast_analyze_python_code(code)
    bas_iss = b_analyze_python_code(code)
    tot_iss = ast_iss + bas_iss

    unique_issues = []
    seen = set()
    for issue in tot_iss:
        key = (
            issue.get("type")
        )

        if key not in seen:
            seen.add(key)
            unique_issues.append(issue)

    r_score = calculate_risk_score(unique_issues)
    r_level = get_risk_level(r_score)
    summary = generate_summary(unique_issues)

    report = {
        "filename": file.filename,
        "status": "analyzed",
        "summary": summary,
        "risk": {
            "score": r_score,
            "level": r_level
        },
        "results": {
            "issues_found": len(unique_issues),
            "issues": unique_issues
        }
    }

    # AI 
    ai_insights = generate_ai_insights(report, call_llm)
    report["ai_insights"] = ai_insights

    saved_path = save_report(report)

    return {
        "status": "saved",
        "saved_to": saved_path,
        "report": report
    }

@app.get("/reports")
def list_reports():

    files = os.listdir(REPORT_FOLDER)

    reports = []

    for f in files:
        file_path = os.path.join(REPORT_FOLDER, f)

        stats = os.stat(file_path)      # TAKE FILE'S INFO
        
        reports.append ({
            "filename": f,
            "path": file_path,
            "size (bytes)": stats.st_size,
            "created time": datetime.fromtimestamp(stats.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
        })

    return {
        "status": "ok",
        "total reports": len(reports),
        "reports": reports
    }