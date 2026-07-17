import json
import re
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")


def compute_expected_report():
    """Compute expected values directly from access.log."""
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

    return {
        "total_requests": total_requests,
        "unique_ips": len(unique_ips),
        "top_path": paths.most_common(1)[0][0],
    }


def load_report():
    assert REPORT_PATH.exists(), "report.json was not created"

    with REPORT_PATH.open() as f:
        return json.load(f)


def test_success_criterion_1_create_report():
    """
    Success Criterion 1:
    Create a valid JSON report at /app/report.json.
    """
    report = load_report()
    assert isinstance(report, dict)


def test_success_criterion_2_required_fields():
    """
    Success Criterion 2:
    Report contains the required fields.
    """
    report = load_report()

    assert set(report.keys()) == {
        "total_requests",
        "unique_ips",
        "top_path",
    }


def test_success_criterion_3_correct_values():
    """
    Success Criterion 3:
    Values match the access log.
    """
    report = load_report()
    expected = compute_expected_report()

    assert report == expected