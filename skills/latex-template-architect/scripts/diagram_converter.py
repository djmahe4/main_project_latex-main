import json
import os

META_PATH = os.getenv("PROJECT_META_PATH", os.path.join("skills", "docs", "extracted_meta.json"))

def list_diagrams():
    if not os.path.exists(META_PATH):
        print("Error: extracted_meta.json not found.")
        return

    with open(META_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    for i, entry in enumerate(data):
        if entry.get("type") == "diagram":
            print(f"--- DIAGRAM {i} FROM {entry['file']} ---")
            print(entry['content'])
            print("--- END DIAGRAM ---")

if __name__ == "__main__":
    list_diagrams()
