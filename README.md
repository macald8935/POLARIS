# POLARIS  
Policy-Oriented Local Audit & Risk Intelligence System  
(NIST Cybersecurity Framework Aligned)

POLARIS is an offline, standards-driven cybersecurity policy analysis and improvement engine.  
It evaluates organizational policies against the **CIS MS-ISAC NIST Cybersecurity Framework Policy Template Guide (2024)** to identify gaps, improve policy language, and generate a structured, NIST-aligned improvement roadmap.

This project was developed as a solution to **PS-1: Local LLM Powered Policy Gap Analysis and Improvement Module**.

---

## Problem Statement

Organizations maintain cybersecurity policies such as ISMS, Data Privacy, Patch Management, and Risk Management.  
However, these policies are often incomplete, inconsistently written, or weakly aligned with recognized standards.

POLARIS addresses this challenge by:
- Identifying policy gaps against the NIST Cybersecurity Framework
- Enhancing policy language to address missing controls
- Providing a phased improvement roadmap aligned with NIST CSF

All analysis is performed **locally and offline**, without the use of external APIs.

---

## Key Features

- Deterministic policy gap analysis aligned with NIST CSF
- Reference controls derived from CIS MS-ISAC Policy Template Guide (2024)
- Local lightweight LLM usage for policy language enhancement only
- Fully offline execution (no cloud services or external APIs)
- NIST function-wise improvement roadmap (Identify, Protect, Detect, Respond, Recover)
- Control Coverage Matrix and policy maturity scoring
- Supports multiple policy domains:
  - ISMS
  - Data Privacy & Security
  - Patch Management
  - Risk Management

---

## Architecture Overview

POLARIS follows a layered, audit-first design:

- **Framework Layer**  
  NIST CSF controls encoded in structured JSON format for deterministic evaluation.

- **Analysis Engine**  
  Clause-level gap detection, scoring, and roadmap generation.

- **LLM Enhancement Layer**  
  A lightweight local LLM is used only to improve policy wording.  
  Gap identification and scoring remain fully deterministic.

- **Output Layer**  
  CLI-based output designed for audit, governance, and compliance review.

---

## Project Structure

```
POLARIS/
│
├── data/
│   ├── frameworks/
│   │   └── nist_cis_controls.json
│   └── sample_policies/
│       ├── isms_policy.txt
│       ├── data_privacy_policy.txt
│       ├── patch_management_policy.txt
│       └── risk_management_policy.txt
│
├── engine/
│   ├── policy_loader.py
│   ├── gap_detector.py
│   ├── policy_rewriter.py
│   ├── roadmap_generator.py
│   └── scorecard.py
│
├── llm/
│   ├── prompts.py
│   └── local_llm.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

## How to Run (Windows – Command Line)

### Prerequisites
- Python 3.10 or higher
- Git
- Windows OS

---

### Step 1: Create and activate virtual environment
```cmd
python -m venv venv
venv\Scripts\activate
```

---

### Step 2: Install dependencies
```cmd
pip install -r requirements.txt
```

---

### Step 3: Install local LLM (one-time setup)
Download Ollama from:  
https://ollama.com/download

Then pull the lightweight model:
```cmd
ollama pull mistral
```

---

### Step 4: Run POLARIS
```cmd
python main.py
```

---

## Output

For each policy, POLARIS produces:
- Control-wise gap analysis
- LLM-enhanced policy improvement text
- Short, mid, and long-term improvement roadmap
- NIST function-wise control coverage matrix
- Overall policy maturity score and maturity level

All output is displayed directly in the terminal.

---

## Reference Standard

- CIS MS-ISAC NIST Cybersecurity Framework Policy Template Guide (2024)  
  https://www.cisecurity.org/

---

## Design Principles and Limitations

- Controls not explicitly documented are treated as missing
- LLM is not used for decision-making or scoring
- Clause matching is keyword-based (semantic matching is a future enhancement)
- CLI-first design, consistent with security and audit tooling practices

---

## Future Enhancements

- Semantic similarity-based gap detection
- PDF and DOCX policy ingestion
- Exportable compliance reports (PDF/DOCX)
- Multi-framework support (ISO 27001, SOC 2, GDPR)

---

## Final Note

POLARIS follows an audit-first philosophy:

**If a control is not documented, it is treated as non-existent.**

This approach mirrors real-world cybersecurity governance and compliance assessments.
