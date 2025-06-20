import json

# Load the CUADv1.json file
with open("data/CUADv1.json", "r") as f:
    data = json.load(f)

# Dive into the first entry in 'data'
first_entry = data["data"][0]
print("📄 Title:", first_entry["title"])

# Explore paragraphs
paragraphs = first_entry["paragraphs"]
print("\nTotal paragraphs in this entry:", len(paragraphs))

# Print first paragraph structure
if paragraphs:
    first_para = paragraphs[0]
    print("\n📝 Paragraph Keys:", first_para.keys())
    print("📜 Context Snippet:", first_para.get("context", "")[:500], "...")  # print first 500 characters
    print("\n🔖 Number of QAs (labels):", len(first_para.get("qas", [])))
    if first_para.get("qas"):
        print("📌 Sample QA:", first_para["qas"][0])
