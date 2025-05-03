import json
from collections import Counter

with open("data/snippets.json", "r", encoding="utf-8") as f:
    snippets = json.load(f)

print(f"🔢 Total Snippets: {len(snippets)}")

# Language distribution
lang_count = Counter(snippet['language'] for snippet in snippets)
print("\n🗂️ Language Distribution:")
for lang, count in lang_count.items():
    print(f"  {lang}: {count}")

# Repo distribution
repo_count = Counter(snippet['repo_name'] for snippet in snippets)
print("\n📁 Repos Used:")
for repo, count in repo_count.items():
    print(f"  {repo}: {count}")

# Preview first snippet
print("\n🔍 Sample Snippet:\n")
sample = snippets[0]
print(f"Repo: {sample['repo_name']}")
print(f"Language: {sample['language']}")
print(f"Path: {sample['path']}")
print(f"Code:\n{sample['code'][:300]}...")  # Just first 300 chars