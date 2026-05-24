from engine.roadmap_generator import generate_roadmap


def test_generate_roadmap_places_findings_by_score():
    findings = [
        {"control": "A", "title": "Missing", "score": 0, "missing": ["one"]},
        {"control": "B", "title": "Weak", "score": 1, "missing": ["two"]},
        {"control": "C", "title": "Partial", "score": 2, "missing": ["three"]},
        {"control": "D", "title": "Covered", "score": 3, "missing": []},
    ]

    roadmap = generate_roadmap(findings)

    assert roadmap["Short Term (0-3 months)"] == ["A - Missing: address 1 missing clause(s)"]
    assert roadmap["Mid Term (3-6 months)"] == ["B - Weak: address 1 missing clause(s)"]
    assert roadmap["Long Term (6-12 months)"] == ["C - Partial: address 1 missing clause(s)"]
