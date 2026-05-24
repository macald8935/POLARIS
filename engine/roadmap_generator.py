"""Improvement roadmap generation."""

from __future__ import annotations


ROADMAP_PHASES = {
    "Short Term (0-3 months)": {0},
    "Mid Term (3-6 months)": {1},
    "Long Term (6-12 months)": {2},
}


def generate_roadmap(findings: list[dict]) -> dict[str, list[str]]:
    roadmap = {phase: [] for phase in ROADMAP_PHASES}

    for finding in findings:
        entry = f"{finding['control']} - {finding.get('title', 'Untitled Control')}"
        if finding.get("missing"):
            entry = f"{entry}: address {len(finding['missing'])} missing clause(s)"

        for phase, scores in ROADMAP_PHASES.items():
            if finding.get("score") in scores:
                roadmap[phase].append(entry)
                break

    return roadmap
