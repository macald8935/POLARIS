import json

from engine.gap_detector import HashingEmbeddingModel, detect_gaps


def test_detect_gaps_semantic_counts(tmp_path):
    framework = {
        "framework": "TEST",
        "version": "1.0",
        "controls": [
            {
                "id": "TST-1",
                "function": "IDENTIFY",
                "name": "Asset Management",
                "description": "Test control",
                "required_clauses": ["asset inventory", "software inventory", "incident response plan"],
            }
        ],
    }
    framework_path = tmp_path / "framework.json"
    framework_path.write_text(json.dumps(framework), encoding="utf-8")

    policy_text = "The organization maintains an asset inventory. A software inventory is reviewed quarterly."
    findings = detect_gaps(policy_text, framework_path, threshold=0.45, model=HashingEmbeddingModel())

    assert len(findings) == 1
    assert findings[0]["score"] == 2
    assert "incident response plan" in findings[0]["missing"]
    assert len(findings[0]["covered"]) == 2


def test_empty_policy_marks_all_clauses_missing(tmp_path):
    framework = {
        "framework": "TEST",
        "version": "1.0",
        "controls": [
            {
                "id": "TST-1",
                "function": "PROTECT",
                "name": "Access",
                "required_clauses": ["least privilege", "access review"],
            }
        ],
    }
    framework_path = tmp_path / "framework.json"
    framework_path.write_text(json.dumps(framework), encoding="utf-8")

    findings = detect_gaps("", framework_path, model=HashingEmbeddingModel())

    assert findings[0]["score"] == 0
    assert findings[0]["missing"] == ["least privilege", "access review"]
