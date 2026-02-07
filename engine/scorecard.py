def generate_scorecard(findings):
    """
    Generates a NIST Function-wise coverage matrix and overall maturity score.
    """

    matrix = {}
    maturity_labels = {
        (0, 20): "Initial",
        (21, 40): "Developing",
        (41, 60): "Defined",
        (61, 80): "Managed",
        (81, 100): "Optimized"
    }

    # Build matrix
    for f in findings:
        func = f["function"]

        if func not in matrix:
            matrix[func] = {
                "total": 0,
                "fully_covered": 0,
                "partially_covered": 0,
                "missing": 0
            }

        matrix[func]["total"] += 1

        if f["score"] == 3:
            matrix[func]["fully_covered"] += 1
        elif f["score"] in [1, 2]:
            matrix[func]["partially_covered"] += 1
        else:
            matrix[func]["missing"] += 1

    # Calculate percentages
    for func in matrix:
        covered = (
            matrix[func]["fully_covered"]
            + matrix[func]["partially_covered"]
        )
        matrix[func]["coverage_percent"] = round(
            (covered / matrix[func]["total"]) * 100, 2
        )

    return matrix, maturity_labels
