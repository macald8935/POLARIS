"""Optional local Ollama integration.

POLARIS never calls external APIs. This module invokes a locally installed
Ollama model only for policy wording suggestions and fails closed to a static
compliance-safe clause when Ollama is unavailable.
"""

from __future__ import annotations

import subprocess

from llm.prompts import POLICY_GAP_REWRITE_PROMPT


def rewrite_with_llm(missing_elements: list[str], timeout: int = 20, model: str = "mistral") -> str:
    prompt = POLICY_GAP_REWRITE_PROMPT.format(
        missing_elements="\n".join(f"- {element}" for element in missing_elements)
    )

    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=timeout,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass

    return (
        "The organization shall formally document and implement the identified missing "
        "controls in alignment with the selected cybersecurity framework. These controls "
        "shall be approved by management, assigned to accountable owners, measured for "
        "effectiveness, and reviewed at least annually."
    )
