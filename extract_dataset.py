from datasets import load_dataset
import json
import os

def create_dataset():
    print("🔄 Loading dataset...")
    try:
        dataset = load_dataset("bigcode/the-stack", language="java", split="train[:1%]")
    except Exception as e:
        print(f"❌ Failed to load dataset: {e}")
        return

    snippets = []
    print("🧠 Extracting code snippets...")
    for item in dataset:
        content = item.get("content", "").strip()
        if content:
            snippets.append({
                "code": content,
                "source": item.get("path", "Unknown")
            })

    output_path = os.path.join("backend", "data", "snippets.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(snippets, f, indent=2)
        print(f"✅ Saved {len(snippets)} code snippets to {output_path}")
    except Exception as e:
        print(f"❌ Failed to write JSON file: {e}")

if __name__ == "__main__":
    create_dataset()
