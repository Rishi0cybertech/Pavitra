from core.scanner import scan_target
from core.reporter import generate_report
from core.analyzer import calculate_risk_score, prioritize_fixes
from datetime import datetime

target = "127.0.0.1"
data = scan_target(target)  # returns a list now

for host in data:
    host["risk_analysis"] = calculate_risk_score(host.get("ports", []))
    host["ports"] = prioritize_fixes(host.get("ports", []))

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"npath_report_{timestamp}.pdf"
generate_report(data, filename)