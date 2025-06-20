import streamlit as st
from PyPDF2 import PdfReader
from summarizer import summarize_text
from clause_extractor import extract_clauses
from legality_checker import check_legality, get_missing_clauses, append_missing_clauses

# Configure the page layout
st.set_page_config(page_title="ClauseLens", layout="centered")

# Sidebar Inputs
st.sidebar.title("📄 ClauseLens Legal Analyzer")
doc_type = st.sidebar.selectbox("Select Document Type", ["NDA", "Lease Agreement", "Employment Contract"])
uploaded_file = st.sidebar.file_uploader("Upload Legal Document (PDF)", type=["pdf"])

# New: User can select what they want to analyze
mode = st.sidebar.radio("Choose Analysis Type", ["Summary", "Clause Analysis", "Similarity Check"])

# Main App Title
st.title("ClauseLens - AI Legal Assistant")

# Check if file is uploaded
if uploaded_file:
    # Extract text from uploaded PDF
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    # Show Document Preview
    st.subheader("📘 Original Document Preview")
    with st.expander("Click to view full text"):
        st.write(text)

    # 1️⃣ SUMMARY
    if mode == "Summary":
        st.subheader("📝 Document Summary")
        summary = summarize_text(text)
        st.success(summary)

    # 2️⃣ CLAUSE ANALYSIS
    elif mode == "Clause Analysis":
        st.subheader("🔍 Extracted Clauses")
        clauses = extract_clauses(text, doc_type)

        if clauses:
            for clause_title, contents in clauses.items():
                for idx, content in enumerate(contents, 1):
                    st.markdown(f"### {clause_title} (Instance {idx})")
                    st.info(content)
        else:
            st.warning("No key clauses were found.")

        # Legality Score
        st.subheader("⚖️ Legality Analysis")
        score = check_legality(text, doc_type)
        missing = get_missing_clauses(text, doc_type)

        st.metric("📊 Legal Completeness", f"{score:.2f}%")
        if missing:
            st.warning("Missing Clauses:")
            for clause in missing:
                st.markdown(f"🔸 {clause}")
        else:
            st.success("✅ All essential clauses present.")

        # Complete the Document
        st.subheader("📄 Complete the Document")
        if st.button("✍️ Append Missing Clauses & Download"):
            completed_text = append_missing_clauses(text, doc_type, missing)

            with open("completed_document.txt", "w", encoding="utf-8") as f:
                f.write(completed_text)

            with open("completed_document.txt", "rb") as f:
                st.download_button(
                    label="⬇️ Download Completed Document",
                    data=f,
                    file_name="completed_document.txt",
                    mime="text/plain"
                )

    # 3️⃣ SIMILARITY CHECK (Placeholder for now)
    elif mode == "Similarity Check":
        st.subheader("🧪 Similarity Check (Experimental)")
        st.info("⚙️ This feature will compare your document to legal clause templates to check for semantic closeness.")
        st.code("similarity_score = calculate_similarity(text, reference_clauses)  # ← To be implemented")

else:
    st.info("👈 Please upload a document from the sidebar.")
