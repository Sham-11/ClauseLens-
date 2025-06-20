import joblib
from nltk.tokenize import sent_tokenize
from clause_templates import clause_templates

model = joblib.load("models/cuad_clause_classifier.pkl")

def chunk_text(text, chunk_size=3):
    sentences = sent_tokenize(text)
    return [" ".join(sentences[i:i+chunk_size]) for i in range(0, len(sentences), chunk_size)]

def extract_clauses(text, doc_type=None):
    chunks = chunk_text(text)
    predicted_clauses = []

    for chunk in chunks:
        prediction = model.predict([chunk])[0]
        clause_text = clause_templates.get(prediction)
        if clause_text:
            predicted_clauses.append({
                'clause': prediction,
                'text': clause_text
            })

    # Deduplicate repeated clauses
    unique_clauses = deduplicate_clauses(predicted_clauses)

    # Convert back to dict format if needed
    results = {}
    for clause in unique_clauses:
        if clause['clause'] not in results:
            results[clause['clause']] = []
        results[clause['clause']].append(clause['text'])

    return results

def deduplicate_clauses(predicted_clauses):
    unique_clauses = {}
    for clause in predicted_clauses:
        key = (clause['clause'], clause['text'])
        if key not in unique_clauses:
            unique_clauses[key] = clause
    return list(unique_clauses.values())
