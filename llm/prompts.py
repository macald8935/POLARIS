"""
prompts.py

This file contains prompt templates for OPTIONAL local LLM usage.
The LLM is NOT used for gap detection or scoring.
It is only intended for controlled language enhancement tasks such as:
- Policy clause rewriting
- Executive summaries
- Improvement explanations

The core compliance logic remains deterministic and framework-driven.
"""

# ============================================================
# PROMPT 1: POLICY GAP REWRITE PROMPT
# ============================================================

POLICY_GAP_REWRITE_PROMPT = """
You are a cybersecurity policy auditor and compliance expert.

Task:
Rewrite the missing policy elements listed below into formal,
professional policy language aligned with the NIST Cybersecurity Framework (NIST CSF).

Rules:
- Do NOT invent new controls
- Do NOT modify existing policy content
- Only write clauses for the missing elements provided
- Use clear, auditable, compliance-safe language
- Keep the tone formal and organization-neutral

Missing Policy Elements:
{missing_elements}

Output:
Provide a concise policy clause suitable for direct inclusion
in an organizational cybersecurity policy document.
"""

# ============================================================
# PROMPT 2: EXECUTIVE SUMMARY PROMPT
# ============================================================

EXECUTIVE_SUMMARY_PROMPT = """
You are a senior cybersecurity consultant preparing an executive summary
for organizational leadership.

Context:
The following findings were identified during a policy gap analysis
against the NIST Cybersecurity Framework.

Findings Summary:
{gap_summary}

Task:
Write a brief executive summary that:
- Explains the current policy maturity
- Highlights major risk areas
- Emphasizes the importance of remediation
- Avoids technical jargon

Tone:
Professional, high-level, business-focused.

Output:
An executive-ready summary suitable for a compliance report.
"""

# ============================================================
# PROMPT 3: IMPROVEMENT ROADMAP EXPLANATION PROMPT
# ============================================================

ROADMAP_EXPLANATION_PROMPT = """
You are a cybersecurity governance advisor.

Task:
Explain the following cybersecurity improvement roadmap
in clear, structured language aligned with NIST CSF principles.

Roadmap:
{roadmap_data}

Rules:
- Do not add new recommendations
- Do not change timelines
- Explain WHY each phase is important
- Keep explanations concise and actionable

Output:
A readable explanation suitable for inclusion in a policy improvement report.
"""

# ============================================================
# PROMPT 4: CONTROL RISK JUSTIFICATION PROMPT
# ============================================================

CONTROL_RISK_JUSTIFICATION_PROMPT = """
You are performing a cybersecurity risk justification.

Control:
{control_id} - {control_title}

Identified Risk:
{risk_statement}

Task:
Explain the security and business impact of not addressing this control.

Rules:
- Keep explanation factual and realistic
- Avoid exaggerated language
- Align with common enterprise risk scenarios

Output:
A short risk justification paragraph suitable for audit documentation.
"""
