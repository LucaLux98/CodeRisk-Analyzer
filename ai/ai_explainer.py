def generate_ai_insights(report, llm_call):
    prompt = f"""
    You are a security expert.

    Analyze this report:
    Isuues: {report.get('unique_issues')}
    Risk score: {report.get('risk_score')}
    Risk level: {report.get('risk_level')}

    Provide:
    - explanation of risks
    - severity
    - fixes
    """
    return llm_call(prompt)