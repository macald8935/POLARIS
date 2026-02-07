from engine.policy_loader import load_policy
from engine.gap_detector import detect_gaps
from engine.policy_rewriter import rewrite_policy
from engine.roadmap_generator import generate_roadmap
from engine.scorecard import generate_scorecard

FRAMEWORK_PATH = "data/frameworks/nist_cis_controls.json"

policies = {
    "ISMS": "data/sample_policies/isms_policy.txt",
    "Data Privacy": "data/sample_policies/data_privacy_policy.txt",
    "Patch Management": "data/sample_policies/patch_management_policy.txt",
    "Risk Management": "data/sample_policies/risk_management_policy.txt"
}

for policy_name, policy_path in policies.items():
    print(f"\n================ {policy_name} POLICY ANALYSIS ================\n")

    policy_text = load_policy(policy_path)
    findings = detect_gaps(policy_text, FRAMEWORK_PATH)

    # ---------------- GAP ANALYSIS ----------------
    print("--- GAP ANALYSIS ---")
    for f in findings:
        print(
            f"{f['control']} | {f['function']} | "
            f"Score: {f['score']} | Missing Clauses: {len(f['missing'])}"
        )

    # ---------------- POLICY IMPROVEMENTS ----------------
    print("\n--- POLICY IMPROVEMENTS (LLM-ENHANCED) ---")
    print(rewrite_policy(findings))

    # ---------------- ROADMAP ----------------
    print("\n--- IMPROVEMENT ROADMAP ---")
    roadmap = generate_roadmap(findings)
    for phase, items in roadmap.items():
        print(f"\n{phase}:")
        for item in items:
            print(f"  - {item}")

    # ---------------- SCORECARD ----------------
    print("\n--- CONTROL COVERAGE MATRIX (NIST FUNCTION-WISE) ---")
    matrix, maturity_labels = generate_scorecard(findings)

    for func, data in matrix.items():
        print(
            f"{func} | Total: {data['total']} | "
            f"Covered: {data['fully_covered'] + data['partially_covered']} | "
            f"Missing: {data['missing']} | "
            f"Coverage: {data['coverage_percent']}%"
        )

    # ---------------- OVERALL MATURITY ----------------
    max_score = len(findings) * 3
    obtained_score = sum(f["score"] for f in findings)
    maturity_percent = round((obtained_score / max_score) * 100, 2)

    maturity_level = "Initial"
    for (low, high), label in maturity_labels.items():
        if low <= maturity_percent <= high:
            maturity_level = label
            break

    print(f"\nOverall Policy Maturity Score: {maturity_percent}%")
    print(f"Overall Policy Maturity Level: {maturity_level}")
