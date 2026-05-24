"""Prompt templates for optional local LLM usage."""

POLICY_GAP_REWRITE_PROMPT = """
You are a cybersecurity policy auditor and compliance expert.

Rewrite the missing policy elements below into concise, formal policy language.

Rules:
- Do not invent controls that are not listed.
- Do not claim implementation evidence exists.
- Use auditable, organization-neutral language.
- Keep the output suitable for direct inclusion in a policy.

Missing Policy Elements:
{missing_elements}
"""


EXECUTIVE_SUMMARY_PROMPT = """
Write an executive summary for a cybersecurity policy gap analysis.

Findings Summary:
{gap_summary}

Keep the summary business-focused, concise, and suitable for leadership.
"""


ROADMAP_EXPLANATION_PROMPT = """
Explain the following cybersecurity improvement roadmap in clear language.

Roadmap:
{roadmap_data}
"""


CONTROL_RISK_JUSTIFICATION_PROMPT = """
Explain the security and business impact of not addressing this control.

Control:
{control_id} - {control_title}

Risk:
{risk_statement}
"""
