from typing import List, Dict
from pathlib import Path
import json

SEVERITY_SCORES = {
    "CRITICAL": 10,
    "HIGH":     7,
    "MEDIUM":   4,
    "LOW":      1,
}

def load_protocol_intel() -> dict:
    path = Path("data/protocol_intel.json")
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def enrich_protocols(protocols: dict) -> dict:
    """
    Takes the raw protocol counter from capture.py's stats["protocols"]
    and attaches intelligence data to each protocol seen.
    Returns dict: {protocol_name: {"count": int, "intel": {...}}}
    """
    intel_db = load_protocol_intel()
    enriched = {}

    for proto, count in protocols.items():
        proto_key = proto.upper()
        intel = intel_db.get(proto_key, {
            "protocol_name": proto,
            "why_seen":      "No intelligence data available for this protocol yet",
            "who_uses":      "N/A",
            "who_exploits":  "Research manually",
            "risk":          "Unknown — investigate",
            "severity":      "MEDIUM",
            "red_flags":     ["No known red flags on file — manual review recommended"],
            "real_world_example": "N/A"
        })
        enriched[proto] = {
            "count": count,
            "intel": intel
        }

    return enriched


def calculate_session_risk(enriched_protocols: dict, suspicious_count: int) -> dict:
    """
    Calculates an overall risk score for the capture session,
    combining protocol-level risk with suspicious port hits.
    Mirrors NPath's calculate_risk_score() structure.
    """
    if not enriched_protocols:
        return {
            "score":      100,
            "risk_level": "SECURE",
            "grade":      "A",
            "summary":    "No traffic captured to analyze."
        }

    total_packets = sum(p["count"] for p in enriched_protocols.values())

    weighted_risk = sum(
        SEVERITY_SCORES.get(p["intel"].get("severity", "MEDIUM"), 4) * p["count"]
        for p in enriched_protocols.values()
    )
    max_possible = SEVERITY_SCORES["CRITICAL"] * max(total_packets, 1)

    base_score = max(0, 100 - int((weighted_risk / max(max_possible, 1)) * 100))

    # Suspicious port hits penalize the score directly — these are
    # confirmed red flags, not just protocol-level baseline risk
    suspicious_penalty = min(suspicious_count * 15, 60)
    final_score = max(0, base_score - suspicious_penalty)

    if final_score >= 90:
        grade, risk_level = "A", "LOW RISK"
    elif final_score >= 75:
        grade, risk_level = "B", "MODERATE RISK"
    elif final_score >= 50:
        grade, risk_level = "C", "HIGH RISK"
    elif final_score >= 25:
        grade, risk_level = "D", "CRITICAL RISK"
    else:
        grade, risk_level = "F", "SEVERE RISK"

    severities_seen = [p["intel"].get("severity", "MEDIUM") for p in enriched_protocols.values()]
    critical = severities_seen.count("CRITICAL")
    high     = severities_seen.count("HIGH")

    summary_parts = [f"{len(enriched_protocols)} protocol(s) observed"]
    if suspicious_count:
        summary_parts.append(f"{suspicious_count} suspicious packet(s) flagged")
    if critical:
        summary_parts.append(f"{critical} critical-severity protocol(s) present")
    if high:
        summary_parts.append(f"{high} high-severity protocol(s) present")

    return {
        "score":      final_score,
        "risk_level": risk_level,
        "grade":      grade,
        "summary":    " · ".join(summary_parts),
    }


def prioritize_protocols(enriched_protocols: dict) -> list:
    """
    Returns protocols sorted by severity, most critical first —
    same pattern as NPath's prioritize_fixes().
    """
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    items = list(enriched_protocols.items())
    return sorted(
        items,
        key=lambda item: severity_order.get(
            item[1]["intel"].get("severity", "MEDIUM"), 2
        )
    )