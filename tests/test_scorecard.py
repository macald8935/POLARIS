from engine.scorecard import calculate_maturity, generate_scorecard, maturity_level


def test_scorecard_groups_by_function():
    findings = [
        {"function": "IDENTIFY", "score": 3},
        {"function": "IDENTIFY", "score": 1},
        {"function": "PROTECT", "score": 0},
    ]

    matrix, labels = generate_scorecard(findings)

    assert labels[(0, 20)] == "Initial"
    assert matrix["IDENTIFY"]["total"] == 2
    assert matrix["IDENTIFY"]["fully_covered"] == 1
    assert matrix["IDENTIFY"]["partially_covered"] == 1
    assert matrix["IDENTIFY"]["coverage_percent"] == 100.0
    assert matrix["PROTECT"]["missing"] == 1


def test_maturity_scoring_logic():
    findings = [{"score": 3}, {"score": 2}, {"score": 0}]

    maturity = calculate_maturity(findings)

    assert maturity["obtained_score"] == 5
    assert maturity["max_score"] == 9
    assert maturity["percent"] == 55.56
    assert maturity["level"] == "Defined"
    assert maturity_level(85) == "Optimized"
