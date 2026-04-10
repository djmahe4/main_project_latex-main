import json
import os
import re
import argparse
import requests
from pathlib import Path

# narrative_expander.py - Narrative Synthesis via Ollama/Llama3
# Transforms FootyDJ metadata into professional academic prose.

META_PATH = "skills/docs/extracted_meta.json"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3:8b"

def call_ollama(prompt):
    """Calls local Ollama instance for text generation."""
    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        return response.json().get("response", "").strip()
    except Exception as e:
        print(f"Ollama error: {e}. Ensure 'ollama serve' is running.")
        return None

def expand_narrative(content, chapter_context):
    """Synthesizes metadata into a professional paragraph."""
    prompt = f"""
    [ROLE] Senior Academic Writer
    [TASK] Convert the following FootyDJ project metadata into a professional narrative paragraph for a LaTeX report.
    [CHAPTER] {chapter_context}
    
    [METADATA]
    {content}
    
    [RULES]
    - strictly NO bullet points.
    - Use scholarly, cohesive language.
    - Preserve technical terms: YOLO, ByteTrack, OSNet, COCOMO, IoU.
    - [COMPLIANCE] Identify any bracketed placeholders like [variable] or [description] in the metadata. 
    - RESOLVE these placeholders into fluent text based on the context. Do NOT leave brackets in the final output.
    - If a placeholder is a generic "insert figure/table here", rewrite it as a graceful transition or reference (e.g., "as illustrated in the subsequent analysis").
    - Output ONLY the final synthesized paragraph.
    """
    
    expansion = call_ollama(prompt)
    if not expansion or "LLM OFFLINE" in expansion:
        return None
    return expansion

def process_all_chapters():
    if not os.path.exists(META_PATH):
        print("Error: Metadata not found.")
        return

    with open(META_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    chapters = {}
    for entry in data:
        ch = entry.get("chapter", "appendices")
        if ch not in chapters: chapters[ch] = []
        chapters[ch].append(entry)

    # UPDATED: Batching metadata for better context
    for ch_id, entries in chapters.items():
        if ch_id in ["INTERNAL", "appendices"]: continue
        
        print(f"Expanding narrative for {ch_id} (Meta-Batching)...")
        
        # Group entries by file for contextual flow
        file_groups = {}
        for entry in entries:
            fname = entry["file"]
            if fname not in file_groups: file_groups[fname] = []
            file_groups[fname].append(entry)
            
        for fname, group_entries in file_groups.items():
            # Combine up to 3 snippets for a cohesive paragraph
            for i in range(0, len(group_entries), 3):
                batch = group_entries[i:i+3]
                combined_meta = "\n".join([e["content"] for e in batch if e["type"] != "narrative"])
                
                if not combined_meta.strip(): continue
                
                narrative = expand_narrative(combined_meta, ch_id)
                
                if narrative:
                    # Update the first entry in batch and mark others as consumed
                    batch[0]["content"] = narrative
                    batch[0]["type"] = "narrative"
                    for leftover in batch[1:]:
                        leftover["content"] = "" 
                        leftover["type"] = "consumed"
                else:
                    print(f"Skipping batch in {ch_id} due to LLM failure.")
    
    # FINAL COMPLIANCE PASS: Surgical Placeholder Removal
    print(">>> Running Final Compliance Pass (Placeholder Cleanup)...")
    for entry in data:
        if entry["type"] == "narrative" and entry["content"]:
            # Check for [ANYTHING]
            placeholders = re.findall(r'\[([a-zA-Z0-9_ -]{3,})\]', entry["content"])
            if placeholders:
                print(f"  - Fixing {len(placeholders)} leftovers in {entry['file']}")
                clean_prompt = f"Fix the following paragraph by resolving or removing these bracketed placeholders: {placeholders}. Output the corrected paragraph only:\n\n{entry['content']}"
                fixed = call_ollama(clean_prompt)
                if fixed:
                    entry["content"] = fixed

    # Save back for synchronization
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("Narrative expansion with batching and compliance complete.")

if __name__ == "__main__":
    process_all_chapters()
