from engine.policy_rewriter import rewrite_policy


def test_rewrite_policy_returns_no_gap_message():
    text = rewrite_policy([{"missing": []}], use_llm=False)

    assert "No missing clauses" in text


def test_rewrite_policy_fallback_lists_missing_elements():
    findings = [{"missing": ["asset inventory", "access review"]}]

    text = rewrite_policy(findings, use_llm=False)

    assert "POLICY ENHANCEMENT" in text
    assert "asset inventory" in text
    assert "access review" in text
