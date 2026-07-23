import os
import re
import json
import argparse
import subprocess
from pathlib import Path

# scan_codebase.py - v4.0 Hardened Extraction & Chapter Mapping
# Adds: Ollama Logical Extraction, Mermaid Detection, Chapter Classification

# Corrected patterns to avoid DOTALL-induced recursion/swallowing
PATTERNS = {
    '.py':   r'(?m)""".*?"""|\'\'\'.*?\'\'\'|^[ \t]*#.*',
    '.c':    r'/\*[\\s\\S]*?\*/|//.*',
    '.cpp':  r'/\*[\\s\\S]*?\*/|//.*',
    '.h':    r'/\*[\\s\\S]*?\*/|//.*',
    '.ino':  r'/\*[\\s\\S]*?\*/|//.*',
    '.js':   r'/\*[\\s\\S]*?\*/|//.*',
    # Improved MD: Headers, Mermaid, Tables, and long lists/paragraphs
    '.md':   r'(?m)^#+.*|```mermaid[\s\S]*?```|(?:^\|.*$\n?)+|(?:^[ \t]*[-*+][ \t]+.*$\n?)+|^(?:(?![#\s]).){100,2000}', 
    '.json': r'^$', # Skip raw content for JSON to avoid bloat
    '.sh':   r'(?m)^[ \t]*#.*',
    '.tex':  r'(?m)^[ \t]*%.*'
}

IGNORE_DIRS = {
    '.git', 'node_modules', 'vendor', '.gemini', 'logs', 'tmp', 'build', 'dist', 
    '__pycache__', '.venv', 'venv', 'env', '.idea', '.vscode', 'out', 'target',
    'main_project_latex-main' # Exclude the LaTeX project folder itself
}

# Comprehensive mapping for all 10 chapters (Priority: File > Folder > Keyword)
CHAPTER_MAP = {
    # --- SPECIFIC FILES ---
    "final_review_ppt.md": "ch2_literature_review",
    "srs.md": "ch3_system_analysis",
    "architecture_2025.md": "ch5_system_design",
    "pipeline_architecture.md": "ch5_system_design",
    "streaming_architecture_final.md": "ch5_system_design",
    "smart_reid_workflow.md": "ch4_methodology",
    "docker_release.md": "ch6_system_implementation",
    "user_guide.md": "ch1_introduction",
    "citations.md": "ch2_literature_review",
    "next_steps.md": "ch9_conclusions",
    "todo.md": "ch9_conclusions",
    "changelog.md": "ch9_conclusions",
    "quick_start.md": "ch1_introduction",
    "readme.md": "ch1_introduction",
    "presentation.md": "ch1_introduction",
    "api.md": "ch3_system_analysis",
    "running_server.md": "ch6_system_implementation",

    # --- FOLDERS (Using Unix-style forward slashes for internal matching) ---
    "app/": "ch6_system_implementation",
    "frontend/": "ch6_system_implementation",
    "config/": "ch6_system_implementation",
    "tests/": "ch7_testing",
    "test/": "ch7_testing",
    "models/": "ch5_system_design",
    "highlights/": "ch10_appendices",
    "screenshots/": "ch10_appendices",
    "assets/": "ch10_appendices",
    "fragments/": "ch4_methodology",
    "docs/": "ch3_system_analysis",
    "benchmarking/": "ch8_results",
    "homography/": "ch8_results",

    # --- KEYWORDS (Fallback) ---
    "dataset": "ch3_system_analysis",
    "training": "ch8_results",
    "accuracy": "ch8_results",
    "results": "ch8_results",
    "evaluation": "ch8_results",
    "metrics": "ch8_results",
    "survey": "ch2_literature_review",
    "design": "ch5_system_design",
    "architecture": "ch5_system_design",
    "implementation": "ch6_system_implementation",
    "test": "ch7_testing",
    "validation": "ch7_testing",
    "conclusion": "ch9_conclusions",
    "future": "ch9_conclusions",
    "pd_": "appendices",
    "daily_diary": "appendices",
    "qna_": "appendices",
    "appendix": "appendices",
    "homography": "ch4_methodology",
    "reid": "ch4_methodology",
    "pipeline": "ch4_methodology",
    "workflow": "ch4_methodology"
}

# Paths to treat as INTERNAL (completely excluded)
INTERNAL_PATHS = ["main_project_latex-main", "chapters/", "preamble/", "scripts/", "docs/mapping_"]

def get_chapter(file_path):
    """Heuristic to determine target chapter based on path. Normalizes slashes for Windows."""
    path_str = str(file_path).replace('\\', '/').lower()
    
    # Check for internal files first
    for internal in INTERNAL_PATHS:
        if internal in path_str:
            return "INTERNAL"

    # Match CHAPTER_MAP
    for key, chapter in CHAPTER_MAP.items():
        if key in path_str:
            return chapter

    return "MISC" # Use MISC instead of defaulting to Ch5 to avoid concentration

def get_ollama_summary(content, model="llama3:8b"):
    """Optional logical summary via local Ollama instance."""
    prompt = f"Summarize the following code/documentation in 1-2 concise sentences for a LaTeX report. Focus on technical purpose:\n\n{content[:2000]}"
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None

def scan(source_path, use_llm=False):
    extracted_data = []
    logical_summaries = {"chapters": {}, "files": []}
    source = Path(source_path).resolve()
    
    for root, dirs, files in os.walk(source):
        # Filter hidden and ignored dirs
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.')]
        
        for file in files:
            file_path = Path(root) / file
            if file.startswith('.'): continue
            
            ext = file_path.suffix.lower()
            
            if ext in PATTERNS:
                try:
                    # Robust reading for large/mixed-encoding projects
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    # Use re.DOTALL explicitly ONLY where we want spanning blocks
                    # But here the PATTERNS use [\s\S] for blocks which is more robust
                    matches = re.finditer(PATTERNS[ext], content)
                    
                    file_summaries = []
                    relative_path = file_path.relative_to(source)
                    target_chapter = get_chapter(relative_path)
                    
                    for match in matches:
                        snippet = match.group(0).strip()
                        if len(snippet) > 10:
                            is_diagram = "mermaid" in snippet.lower()
                            is_table = snippet.startswith('|') and snippet.count('|') > 2
                            is_list = any(snippet.startswith(prefix) for prefix in ['-', '*', '+']) or re.match(r'^\d+\.', snippet)
                            
                            item_type = "comment"
                            if is_diagram: item_type = "diagram"
                            elif is_table: item_type = "table"
                            elif is_list: item_type = "list"
                            
                            # ISOLATION: Move raw code files to appendices
                            target_chapter = get_chapter(relative_path)
                            if ext in ['.py', '.js', '.c', '.cpp', '.h', '.ino'] and target_chapter != "INTERNAL":
                                target_chapter = "appendices"

                            extracted_data.append({
                                "file": str(relative_path),
                                "language": ext[1:],
                                "content": snippet,
                                "type": item_type,
                                "chapter": target_chapter
                            })
                            
                            if is_diagram:
                                if target_chapter not in logical_summaries["chapters"]:
                                    logical_summaries["chapters"][target_chapter] = {"files": [], "diagrams": []}
                                logical_summaries["chapters"][target_chapter]["diagrams"].append({
                                    "source": str(relative_path),
                                    "content": snippet
                                })

                    # Logical Summary per File (always populated)
                    summary_text = "Auto-extracted from codebase."
                    if use_llm and file_summaries:
                        llm_summary = get_ollama_summary("\n".join(file_summaries))
                        if llm_summary:
                            summary_text = llm_summary
                    
                    logical_summaries["files"].append({
                        "file": str(relative_path),
                        "chapter": target_chapter,
                        "summary": summary_text
                    })
                    
                    if target_chapter not in logical_summaries["chapters"]:
                        logical_summaries["chapters"][target_chapter] = {"files": [], "diagrams": []}
                    logical_summaries["chapters"][target_chapter]["files"].append(str(relative_path))
                            
                except Exception as e:
                    print(f"Warning: Could not read {file_path}: {e}")
                    
    return extracted_data, logical_summaries

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="LaTeX Architect - Hardened Extraction Engine (v4.0)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--source", default=".", help="Directory to scan")
    parser.add_argument("--output", default="docs/extracted_meta.json", help="Path for raw metadata")
    parser.add_argument("--summary", default="docs/logical_summaries.json", help="Path for AI summaries")
    parser.add_argument("--llm", action="store_true", help="Enable Ollama-based logical extraction")
    parser.add_argument("--ignore", nargs="+", default=list(IGNORE_DIRS), help="Directories to ignore")
    args = parser.parse_args()
    
    if args.ignore:
        IGNORE_DIRS = set(args.ignore)
    
    print(f">>> Architect Scan Initialized: {args.source} {'(LLM ON)' if args.llm else ''}")
    data, summaries = scan(args.source, use_llm=args.llm)
    
    project_root = Path(__file__).parents[2] # parents[2] of scripts is /main_project_latex-main/skills
    
    # Save Raw Metadata
    output_meta = project_root / args.output
    output_meta.parent.mkdir(parents=True, exist_ok=True)
    with open(output_meta, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        
    # Save Logical Summaries
    output_sum = project_root / args.summary
    output_sum.parent.mkdir(parents=True, exist_ok=True) # Ensure subdir exists
    with open(output_sum, 'w', encoding='utf-8') as f:
        json.dump(summaries, f, indent=2)
        
    print(f">>> Hardened Extraction Complete. Found {len(data)} insights.")
    print(f">>> Metadata: {output_meta} | Summaries: {output_sum}")
