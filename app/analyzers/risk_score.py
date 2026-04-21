def calculate_risk_score(issues):
    score = 0
    seen = set()

    for issue in issues:        # AVOID DUPLICATE
        key = (
            issue.get("type", ""),
            issue.get("description", "")
        )

        if key in seen:
            continue

        seen.add(key)

        severity = issue.get("severity", "").lower()

        if severity == "high":
            score += 60
        elif severity == "medium":
            score += 30
        elif severity == "low":
            score += 15

    return min(score, 100)      # MAX 100 SCORE