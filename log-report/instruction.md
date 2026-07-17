Analyze the Apache-style access log located at /app/access.log.

Generate a JSON report at /app/report.json.

Success criteria:

1. Create a valid JSON file at /app/report.json.
2. The JSON object must contain exactly these fields:
   - total_requests
   - unique_ips
   - top_path
3. The values of total_requests, unique_ips, and top_path must be computed from /app/access.log and match its contents exactly.