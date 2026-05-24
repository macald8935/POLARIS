"""LLM-assisted policy improvement text generation."""

from __future__ import annotations

from llm.local_llm import rewrite_with_llm


def rewrite_policy(findings: list[dict], use_llm: bool = True) -> str:
    missing_elements = sorted({clause for finding in findings for clause in finding.get("missing", [])})

    if not missing_elements:
        return "No missing clauses were identified. Existing policy language appears aligned."

    llm_text = rewrite_with_llm(missing_elements) if use_llm else _fallback_text(missing_elements)

    return f"POLICY ENHANCEMENT (LLM-GENERATED)\n\n{llm_text}"


def _fallback_text(missing_elements: list[str]) -> str:
    clauses = "; ".join(missing_elements)
    return (
        "The organization shall formally document, approve, implement, and periodically "
        f"review the following policy requirements: {clauses}."
    )
