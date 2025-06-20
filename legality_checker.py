def check_legality(text, doc_type):
    clause_requirements = {
        "NDA": ["Confidentiality", "Non-Disclosure", "Term", "Governing Law", "Termination"],
        "Lease Agreement": ["Rent", "Security Deposit", "Maintenance", "Utilities", "Termination"],
        "Employment Contract": ["Duties", "Compensation", "Leave Policy", "Termination", "Non-Compete"]
    }

    required = clause_requirements.get(doc_type, [])
    found = [clause for clause in required if clause.lower() in text.lower()]
    
    if not required:
        return 0.0
    return round((len(found) / len(required)) * 100, 2)

def get_missing_clauses(text, doc_type):
    clause_requirements = {
        "NDA": ["Confidentiality", "Non-Disclosure", "Term", "Governing Law", "Termination"],
        "Lease Agreement": ["Rent", "Security Deposit", "Maintenance", "Utilities", "Termination"],
        "Employment Contract": ["Duties", "Compensation", "Leave Policy", "Termination", "Non-Compete"]
    }

    required = clause_requirements.get(doc_type, [])
    missing = [clause for clause in required if clause.lower() not in text.lower()]
    return missing

from clause_templates import clause_templates

def append_missing_clauses(text, doc_type, missing_clauses):
    appended = "\n\n--- Auto-Generated Clauses ---\n"
    for clause in missing_clauses:
        if clause in clause_templates:
            appended += f"\n\n{clause_templates[clause]}"
    return text + appended
