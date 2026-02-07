def generate_roadmap(findings):
    roadmap = {
        "Short Term (0–3 months)": [],
        "Mid Term (3–6 months)": [],
        "Long Term (6–12 months)": []
    }

    for f in findings:
        entry = f"{f['control']} - {f['title']}"

        if f["score"] == 0:
            roadmap["Short Term (0–3 months)"].append(entry)
        elif f["score"] == 1:
            roadmap["Mid Term (3–6 months)"].append(entry)
        elif f["score"] == 2:
            roadmap["Long Term (6–12 months)"].append(entry)

    return roadmap
