import pytest

from engine.policy_loader import load_policy


def test_load_txt_policy(tmp_path):
    policy = tmp_path / "policy.txt"
    policy.write_text("Asset Inventory\nLeast Privilege", encoding="utf-8")

    assert load_policy(policy) == "asset inventory\nleast privilege"


def test_load_docx_policy(tmp_path):
    pytest.importorskip("docx")
    from docx import Document

    policy = tmp_path / "policy.docx"
    document = Document()
    document.add_paragraph("Incident Response Plan")
    document.save(policy)

    assert "incident response plan" in load_policy(policy)


def test_load_pdf_policy_strips_repeated_footer(tmp_path):
    pytest.importorskip("pdfplumber")
    pytest.importorskip("reportlab")
    from reportlab.lib.pagesizes import LETTER
    from reportlab.pdfgen import canvas

    policy = tmp_path / "policy.pdf"
    pdf = canvas.Canvas(str(policy), pagesize=LETTER)
    for page in range(3):
        pdf.drawString(72, 740, "POLARIS Confidential")
        pdf.drawString(72, 700, f"Policy body page {page} with asset inventory")
        pdf.drawString(72, 40, "Page Footer")
        pdf.showPage()
    pdf.save()

    text = load_policy(policy)

    assert "asset inventory" in text
    assert "polaris confidential" not in text
    assert "page footer" not in text


def test_unsupported_policy_format(tmp_path):
    policy = tmp_path / "policy.md"
    policy.write_text("# Policy", encoding="utf-8")

    with pytest.raises(ValueError):
        load_policy(policy)
