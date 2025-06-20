from transformers import pipeline

# Load model once
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_text(text):
    if len(text) < 50:
        return "Text too short to summarize."
    
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    summary = ""

    for chunk in chunks:
        result = summarizer(chunk, max_length=150, min_length=30, do_sample=False)
        summary += result[0]['summary_text'] + " "

    return summary.strip()
