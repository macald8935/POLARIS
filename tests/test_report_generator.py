from output.report_generator import build_report_payload, export_json, export_pdf


def test_pdf_generation_does_not_crash(tmp_path):
    findings = [
        {
            "control": "GV.OC-01",
            "title": "Organizational Context",
            "function": "GOVERN",
            "score": 2,
            "missing": ["external dependencies"],
        }
    ]
    roadmap = {"Short Term (0-3 months)": [], "Mid Term (3-6 months)": [], "Long Term (6-12 months)": ["GV.OC-01"]}
    scorecard = {
        "GOVERN": {
            "total": 1,
            "fully_covered": 0,
            "partially_covered": 1,
            "missing": 0,
            "coverage_percent": 100.0,
            "average_score": 2.0,
        }
    }
    payload = build_report_payload("Sample Policy", "NIST_CSF", findings, roadmap, scorecard, "Add missing clauses.")

    pdf_path = export_pdf(payload, tmp_path / "report.pdf")
    json_path = export_json(payload, tmp_path / "report.json")

    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 0
    assert json_path.exists()
