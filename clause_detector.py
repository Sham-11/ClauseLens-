# clause_detector.py

from clause_extractor import CLAUSE_TEMPLATES

# Dummy completions (for demo purpose)
CLAUSE_COMPLETIONS = {
    "Confidentiality": "The parties agree to keep all information confidential.",
    "Non-Disclosure": "No party shall disclose any information without written consent.",
    "Termination Clause": "Either party may terminate the contract with 30 days' notice.",
    "Governing Law": "This agreement shall be governed by the laws of India.",
    "Job Role": "The employee shall serve as a Software Engineer under company terms.",
    # Add more completions for demo
}

def detect_missing_clauses(text, doc_type):
    expected_clauses = CLAUSE_TEMPLATES.get(doc_type, [])
    present_clauses = [clause for clause in expected_clauses if clause.lower() in text.lower()]
    missing_clauses = list(set(expected_clauses) - set(present_clauses))
    
    percent_legal = (len(present_clauses) / len(expected_clauses)) * 100 if expected_clauses else 0

    completed_text = text + "\n\n" + "\n".join(
        [f"[{clause}]: {CLAUSE_COMPLETIONS.get(clause, 'Clause not found.')}" for clause in missing_clauses]
    )

    return percent_legal, missing_clauses, completed_text
