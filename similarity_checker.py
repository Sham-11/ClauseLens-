from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from clause_templates import clause_templates  # dictionary of standard clauses

def compute_similarity(text, clause_name):
    standard_text = clause_templates.get(clause_name)
    if not standard_text:
        return 0.0
    
    vectorizer = TfidfVectorizer().fit_transform([text, standard_text])
    similarity_matrix = cosine_similarity(vectorizer[0:1], vectorizer[1:2])
    return float(similarity_matrix[0][0] * 100)

def check_all_clause_similarities(extracted_clauses):
    clause_scores = {}

    for clause_name, instances in extracted_clauses.items():
        avg_score = 0
        for instance_text in instances:
            score = compute_similarity(instance_text, clause_name)
            avg_score += score
        avg_score /= len(instances)
        clause_scores[clause_name] = round(avg_score, 2)

    return clause_scores
