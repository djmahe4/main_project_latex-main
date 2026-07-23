import json
import re
from pathlib import Path

# propose_mappings.py - Heuristic Extraction for LaTeX Architect
# Targets: Project Title, Students, Reg IDs, Guide

ROOT_DIR = Path(__file__).parents[2] # parents[2] of scripts is /main_project_latex-main/skills
META_PATH = ROOT_DIR / "docs/extracted_meta.json"
SUM_PATH = ROOT_DIR / "docs/logical_summaries.json"
PROPOSAL_PATH = ROOT_DIR / "docs/mapping_proposals.json"

def extract_heuristics(data, summaries=None):
    proposals = {
        "tplProjectTitle": "[project_title]",
        "tplStudentA": "",
        "tplRegA": "",
        "tplStudentB": "",
        "tplRegB": "",
        "tplStudentC": "",
        "tplRegC": "",
        "tplStudentD": "",
        "tplRegD": "",
        "tplProjectGuide": ""
    }
    
    students = []
    
    # Use AI Logical Summaries if available to improve context
    if summaries and "files" in summaries:
        for s_item in summaries["files"]:
            sum_text = s_item.get("summary", "").lower()
            if "project" in sum_text and "title" in sum_text:
                # Potential title discovery from summary
                match = re.search(r'title is\s*"(.*)"', sum_text)
                if match: proposals["tplProjectTitle"] = match.group(1).title()

    # Original heuristic for Project Title and Students
    sorted_items = sorted(data, key=lambda x: (0 if '.md' in x['file'] else 1, x['file']))
    
    for item in sorted_items:
        content = item.get('content', '')
        file_name = item.get('file', '').lower()
        
        if 'latex-template-architect' in file_name: continue
            
        # 1. Project Title
        if "title" in content and (proposals["tplProjectTitle"].startswith("[") or proposals["tplProjectTitle"] == "[project_title]"):
            title_match = re.search(r'#\s*(<project_title>.*)', content, re.I)
            if title_match:
                proposals["tplProjectTitle"] = title_match.group(1).split('\n')[0].strip().strip('*').rstrip(')')
            
        # 2. Student Discovery
        student_match = re.search(r'Individual Project Diary [–-]\s*(.*)', content, re.I)
        if not student_match and file_name.startswith('pd_'):
            student_match = re.search(r'^##\s*([A-Za-z ]+)', content, re.MULTILINE)
        
        if student_match:
            name = student_match.group(1).split('\n')[0].strip().strip('*').strip().rstrip(')')
            if name not in students and len(name) > 3 and "Name" not in name and "[" not in name:
                students.append(name)
                
    # Assign students
    for i, name in enumerate(sorted(students)[:4]):
        proposals[f"tplStudent{chr(65+i)}"] = name
        
    return proposals

if __name__ == "__main__":
    if not META_PATH.exists():
        print("Error: extracted_meta.json not found.")
        exit(1)
        
    with open(META_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    summaries = None
    if SUM_PATH.exists():
        with open(SUM_PATH, 'r', encoding='utf-8') as f:
            summaries = json.load(f)
        
    mappings = extract_heuristics(data, summaries)
    
    # Save for manual verification
    with open(PROPOSAL_PATH, 'w', encoding='utf-8') as f:
        json.dump(mappings, f, indent=2)
        
    print(f">>> Heuristic mapping complete. File saved to {PROPOSAL_PATH.name}")
    print(">>> Mapping Proposals Found:")
    for k, v in mappings.items():
        if v:
            print(f"  {k}: {v}")
