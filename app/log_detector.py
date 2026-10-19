
from collections import Counter
from pathlib import Path
import re

LOG_FILE = Path("evidence/security-events.log")
REPORT_FILE = Path("reports/security-alerts.txt")

failed_logins = Counter()
alerts = []

if not LOG_FILE.exists():
    raise SystemExit(f"Log file not found: {LOG_FILE}")

for line in LOG_FILE.read_text(encoding="utf-8").splitlines():
    if "result=failed" in line and "auth" in line:
        match = re.search(r"\bsrc=([^\s]+)", line)
        source = match.group(1) if match else "unknown"
        failed_logins[source] += 1

    if "ALERT" in line:
        alerts.append(f"Existing alert: {line}")

for source, count in failed_logins.items():
    if count >= 3:
        alerts.append(
            f"BRUTE-FORCE INDICATOR: {count} failed logins from {source}"
        )

REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
REPORT_FILE.write_text(
    "SIL SECURITY MONITORING LAB\n"
    "Synthetic log analysis only\n\n"
    + ("\n".join(alerts) if alerts else "No alerts detected.")
    + "\n",
    encoding="utf-8",
)

print(f"Analysed log file: {LOG_FILE}")
print(f"Failed-login sources: {dict(failed_logins)}")
print(f"Alerts generated: {len(alerts)}")
print(f"Report saved: {REPORT_FILE}")
