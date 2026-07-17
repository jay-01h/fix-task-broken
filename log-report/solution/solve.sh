#!/bin/bash
set -euo pipefail

python3 - <<'PY'
import json, re
from collections import Counter
from pathlib import Path

LOG_PATH = Path("/app/access.log")
REPORT_PATH = Path("/app/report.json")

total_requests = 0
unique_ips = set()
paths = Counter()

with LOG_PATH.open() as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        total_requests += 1
        unique_ips.add(line.split()[0])
        match = re.search(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ', line)
        if match:
            paths[match.group(1)] += 1

report = {
    "total_requests": total_requests,
    "unique_ips": len(unique_ips),
    "top_path": paths.most_common(1)[0][0],
}

REPORT_PATH.write_text(json.dumps(report, indent=2))
PY