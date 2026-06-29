from typing import List, Dict

# Risk scoring weights
SEVERITY_SCORES = {
    "CRITICAL": 10,
    "HIGH":     7,
    "MEDIUM":   4,
    "LOW":      1,
}

def calculate_risk_score(ports: List[Dict]) -> Dict:
    """
    Calculate overall risk score based on open ports and their severity.
    Returns score out of 100 and risk level.
    """
    if not ports:
        return {
            "score":      100,
            "risk_level": "SECURE",
            "grade":      "A",
            "summary":    "No open ports detected. System appears well-configured."
        }

    total_weight  = sum(SEVERITY_SCORES.values()) * len(ports)
    actual_weight = sum(
        SEVERITY_SCORES.get(p["intel"].get("severity", "MEDIUM"), 4)
        for p in ports
    )

    # Score = inverse of risk (100 = perfect, 0 = worst)
    raw_score = max(0, 100 - int((actual_weight / max(total_weight, 1)) * 100))

    # Determine grade
    if raw_score >= 90:
        grade      = "A"
        risk_level = "LOW RISK"
    elif raw_score >= 75:
        grade      = "B"
        risk_level = "MODERATE RISK"
    elif raw_score >= 50:
        grade      = "C"
        risk_level = "HIGH RISK"
    elif raw_score >= 25:
        grade      = "D"
        risk_level = "CRITICAL RISK"
    else:
        grade      = "F"
        risk_level = "SEVERE RISK"

    # Count severities
    severities = [p["intel"].get("severity", "MEDIUM") for p in ports]
    critical   = severities.count("CRITICAL")
    high       = severities.count("HIGH")
    medium     = severities.count("MEDIUM")
    low        = severities.count("LOW")

    # Summary
    issues = []
    if critical: issues.append(f"{critical} critical issue{'s' if critical > 1 else ''}")
    if high:     issues.append(f"{high} high severity issue{'s' if high > 1 else ''}")
    if medium:   issues.append(f"{medium} medium severity issue{'s' if medium > 1 else ''}")
    if low:      issues.append(f"{low} low severity issue{'s' if low > 1 else ''}")

    summary = f"Found {len(ports)} open port{'s' if len(ports) > 1 else ''} with {', '.join(issues)}."

    return {
        "score":      raw_score,
        "risk_level": risk_level,
        "grade":      grade,
        "summary":    summary,
        "breakdown": {
            "critical": critical,
            "high":     high,
            "medium":   medium,
            "low":      low,
        }
    }


def prioritize_fixes(ports: List[Dict]) -> List[Dict]:
    """
    Return ports sorted by severity — most critical first.
    """
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    return sorted(
        ports,
        key=lambda p: severity_order.get(
            p["intel"].get("severity", "MEDIUM"), 2
        )
    )