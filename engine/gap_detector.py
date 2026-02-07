import json

def detect_gaps(policy_text, framework_path):
    with open(framework_path, "r", encoding="utf-8") as f:
        controls = json.load(f)

    findings = []

    for control_id, control in controls.items():
        missing = []

        for clause in control["required_clauses"]:
            if clause.lower() not in policy_text:
                missing.append(clause)

        total_clauses = len(control["required_clauses"])
        present_clauses = total_clauses - len(missing)

        # Partial scoring logic (0–3)
        coverage_ratio = present_clauses / total_clauses

        if coverage_ratio == 0:
            score = 0
        elif coverage_ratio < 0.5:
            score = 1
        elif coverage_ratio < 1:
            score = 2
        else:
            score = 3

        findings.append({
            "control": control_id,
            "title": control["title"],
            "function": control["function"],
            "missing": missing,
            "score": score,
            "risk": control["risk_if_missing"]
        })

    return findings
