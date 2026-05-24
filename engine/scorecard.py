"""Scorecard and maturity calculations."""

from __future__ import annotations


MATURITY_LABELS = {
    (0, 20): "Initial",
    (21, 40): "Developing",
    (41, 60): "Defined",
    (61, 80): "Managed",
    (81, 100): "Optimized",
}


def calculate_maturity(findings: list[dict]) -> dict:
    max_score = len(findings) * 3
    obtained_score = sum(finding.get("score", 0) for finding in findings)
    percent = round((obtained_score / max_score) * 100, 2) if max_score else 0.0
    level = maturity_level(percent)
    return {
        "obtained_score": obtained_score,
        "max_score": max_score,
        "percent": percent,
        "level": level,
    }


def maturity_level(percent: float) -> str:
    for (low, high), label in MATURITY_LABELS.items():
        if low <= percent <= high:
            return label
    return "Optimized" if percent > 100 else "Initial"


def generate_scorecard(findings: list[dict]):
    """Generate framework function-wise coverage and maturity labels."""

    matrix: dict[str, dict] = {}

    for finding in findings:
        function = finding.get("function", "Unknown")
        matrix.setdefault(
            function,
            {
                "total": 0,
                "fully_covered": 0,
                "partially_covered": 0,
                "missing": 0,
                "coverage_percent": 0.0,
                "average_score": 0.0,
            },
        )

        matrix[function]["total"] += 1
        matrix[function].setdefault("_score_sum", 0)
        matrix[function]["_score_sum"] += finding.get("score", 0)

        if finding.get("score") == 3:
            matrix[function]["fully_covered"] += 1
        elif finding.get("score") in {1, 2}:
            matrix[function]["partially_covered"] += 1
        else:
            matrix[function]["missing"] += 1

    for function, data in matrix.items():
        covered = data["fully_covered"] + data["partially_covered"]
        data["coverage_percent"] = round((covered / data["total"]) * 100, 2)
        data["average_score"] = round(data.pop("_score_sum") / data["total"], 2)

    return matrix, MATURITY_LABELS
