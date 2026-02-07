import subprocess
from llm.prompts import POLICY_GAP_REWRITE_PROMPT

def rewrite_with_llm(missing_elements, timeout=15):
    """
    Uses a lightweight local LLM (Ollama Mistral).
    Falls back safely if LLM is slow or unavailable.
    """

    prompt = POLICY_GAP_REWRITE_PROMPT.format(
        missing_elements=", ".join(missing_elements)
    )

    try:
        result = subprocess.run(
            ["ollama", "run", "mistral"],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=timeout
        )

        if result.stdout.strip():
            return result.stdout.strip()

        raise Exception("Empty LLM response")

    except Exception:
        # SAFE FALLBACK (still compliant)
        return (
            "The organization shall formally document and implement the "
            "identified missing controls in alignment with the NIST "
            "Cybersecurity Framework. These controls shall be approved by "
            "management and reviewed periodically."
        )
