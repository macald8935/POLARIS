from llm.local_llm import rewrite_with_llm

def rewrite_policy(findings):
    all_missing = []

    for f in findings:
        all_missing.extend(f["missing"])

    # Remove duplicates
    all_missing = list(set(all_missing))

    llm_text = rewrite_with_llm(all_missing)

    return f"""
--- POLICY ENHANCEMENT (LLM-GENERATED) ---
{llm_text}
"""
