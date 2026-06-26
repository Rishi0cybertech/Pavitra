from core.scanner import scan_target
from core.reporter import generate_report
from datetime import datetime

target = "127.0.0.1"
data   = scan_target(target)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename  = f"npath_report_{timestamp}.pdf"

generate_report(data, filename)
