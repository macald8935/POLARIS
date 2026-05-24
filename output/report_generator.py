"""PDF and JSON report generation for POLARIS."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from engine.scorecard import calculate_maturity


OUTPUT_DIR = Path("outputs")


def build_report_payload(
    policy_name: str,
    framework: str,
    findings: list[dict],
    roadmap: dict[str, list[str]],
    scorecard: dict[str, dict],
    improvements: str,
) -> dict[str, Any]:
    maturity = calculate_maturity(findings)
    return {
        "tool": "POLARIS",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "policy_name": policy_name,
        "framework": framework,
        "maturity": maturity,
        "stats": {
            "controls": len(findings),
            "fully_covered": sum(1 for finding in findings if finding.get("score") == 3),
            "partially_covered": sum(1 for finding in findings if finding.get("score") in {1, 2}),
            "missing": sum(1 for finding in findings if finding.get("score") == 0),
            "missing_clauses": sum(len(finding.get("missing", [])) for finding in findings),
        },
        "findings": findings,
        "roadmap": roadmap,
        "scorecard": scorecard,
        "policy_improvements": improvements,
    }


def export_json(payload: dict[str, Any], output_path: str | Path | None = None) -> Path:
    path = _resolve_output_path(output_path, payload["policy_name"], "json")
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def export_pdf(payload: dict[str, Any], output_path: str | Path | None = None) -> Path:
    path = _resolve_output_path(output_path, payload["policy_name"], "pdf")
    doc = SimpleDocTemplate(str(path), pagesize=LETTER, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=8, leading=10))
    story = []

    maturity = payload["maturity"]
    story.extend(
        [
            Paragraph("POLARIS", styles["Title"]),
            Paragraph("Policy Offline Lens for Assessment, Risk, and Improvement Scoring", styles["BodyText"]),
            Spacer(1, 0.25 * inch),
            Paragraph(f"Policy: {payload['policy_name']}", styles["Heading2"]),
            Paragraph(f"Framework: {payload['framework']}", styles["BodyText"]),
            Paragraph(f"Generated: {payload['generated_at']}", styles["BodyText"]),
            Spacer(1, 0.3 * inch),
            Paragraph(f"Maturity Score: {maturity['percent']}% ({maturity['level']})", styles["Heading1"]),
            PageBreak(),
        ]
    )

    story.append(Paragraph("1. Executive Summary", styles["Heading1"]))
    stats = payload["stats"]
    summary = (
        f"POLARIS assessed {stats['controls']} controls and identified "
        f"{stats['missing_clauses']} missing clauses. The current maturity level is "
        f"{maturity['level']} with an overall score of {maturity['percent']}%."
    )
    story.append(Paragraph(summary, styles["BodyText"]))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("2. Gap Analysis", styles["Heading1"]))
    gap_rows = [["Control", "Function", "Score", "Missing Clauses"]]
    for finding in payload["findings"]:
        missing = ", ".join(finding.get("missing", [])) or "None"
        gap_rows.append([finding["control"], finding["function"], str(finding["score"]), Paragraph(missing, styles["Small"])])
    story.append(_styled_table(gap_rows, [0.9 * inch, 1.0 * inch, 0.55 * inch, 4.25 * inch]))

    story.append(Paragraph("3. Improvement Roadmap", styles["Heading1"]))
    roadmap_rows = [["Phase", "Recommended Actions"]]
    for phase, items in payload["roadmap"].items():
        roadmap_rows.append([phase, Paragraph("<br/>".join(items) if items else "No immediate action.", styles["Small"])])
    story.append(_styled_table(roadmap_rows, [1.7 * inch, 5.0 * inch]))

    story.append(Paragraph("4. Function Coverage Matrix", styles["Heading1"]))
    matrix_rows = [["Function", "Total", "Covered", "Missing", "Coverage"]]
    for function, data in payload["scorecard"].items():
        covered = data["fully_covered"] + data["partially_covered"]
        matrix_rows.append([function, data["total"], covered, data["missing"], f"{data['coverage_percent']}%"])
    story.append(_styled_table(matrix_rows, [1.4 * inch, 0.8 * inch, 0.9 * inch, 0.9 * inch, 1.0 * inch]))

    story.append(Paragraph("5. LLM-Enhanced Policy Improvements", styles["Heading1"]))
    story.append(Paragraph(payload["policy_improvements"].replace("\n", "<br/>"), styles["BodyText"]))

    doc.build(story)
    return path


def _resolve_output_path(output_path: str | Path | None, policy_name: str, extension: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if output_path:
        path = Path(output_path)
        if path.suffix.lower() != f".{extension}":
            path = path.with_suffix(f".{extension}")
        if not path.is_absolute():
            path = Path.cwd() / path
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(character if character.isalnum() else "_" for character in policy_name).strip("_").lower()
    return OUTPUT_DIR / f"{safe_name}_{timestamp}.{extension}"


def _styled_table(rows: list[list[Any]], widths: list[float]) -> Table:
    table = Table(rows, colWidths=widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#d1d5db")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f9fafb")]),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table
