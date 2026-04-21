# CodeRisk Analyzer

AI-assisted static security analysis tool for Python code.

CodeRisk Analyzer scans Python source code, detects potentially dangerous patterns, computes a risk score and generates structured reports.
It also provides optional AI-generated insights to explain vulnerabilities and suggest improvements.

---

## Features

- Static code analysis using AST parsing
- Detection of risky patterns (e.g. eval, exec, hardcoded secrets)
- Risk scoring system (low / medium / high)
- Deduplication of detected issues
- Structured JSON report generation
- Report persistence (history of analyses)
- Optional AI-powered explanations of detected risks
- Storing of JSON reports

---

## Architecture

The project is modular and organized as follows:

- `main.py` → API entry point (FastAPI)
- `app/analyzers/` → static analysis logic
- `ai/` → AI explanation layer (optional)
- `TEST/` → Few tests to try
- `REPORT/` → stored JSON reports

---

## How it works

1. Upload a Python file via API 
2. Code is analyzed for risky patterns
3. Issues are extracted and deduplicated
4. Risk score and risk level are computed
5. A structured report is generated
6. (Optional) AI generates human-readable insights
7. JSON report is saved for future reference

---

### Analyze file

```bash
POST /analyze-file-report & AI

## Example Request: curl

curl -X POST "http://127.0.0.1:8000/analyze-file-report" \
-F "file=@test.py"

## Example response: output

{
  "status": "saved",
  "saved_to": "REPORT\\report_20260421_175729.json",
  "report": {
    "filename": "TEST 4 - MIXED REAL WORLD.py",
    "status": "analyzed",
    "summary": "Potential code injection risks detected.",
    "risk": {
      "score": 100,
      "level": "high"
    },
    "results": {
      "issues_found": 3,
      "issues": [
        {
          "type": "dangerous function",
          "severity": "high",
          "description": "exec() use detected!"
        },
        {
          "type": "API Key Exposure",
          "severity": "high",
          "description": "Token/API key inside the code"
        },
        {
          "type": "User Input",
          "severity": "low",
          "description": "Input() detected"
        }
      ]
    },
    "ai_insights": "AI disabled (mock response for testing)"
  }
}
