import os
import re
import json
import argparse
from pathlib import Path

# scan_codebase.py - v3.5 Python-Powered Extraction Engine
# Supports: .py, .c, .cpp, .h, .ino, .js, .md, .sh

# Patterns for each language
PATTERNS = {
    '.py':  r'(?s)""".*?"""|\'\'\'.*?\'\'\'|#.*',
    '.c':   r'(?s)/\*.*?\*/|//.*',
    '.cpp': r'(?s)/\*.*?\*/|//.*',
    '.h':   r'(?s)/\*.*?\*/|//.*',
    '.ino': r'(?s)/\*.*?\*/|//.*',
    '.js':  r'(?s)/\*.*?\*/|//.*',
    '.md':  r'(?s)```mermaid.*?```',
    '.sh':  r'#.*'
}

IGNORE_DIRS = {".git", "node_modules", "vendor", ".gemini", "Preamble", "frontmatter", "chapters", "examples", "docs", "assets", "skills"}

def scan(source_path, project_root):
    extracted_data = []
    source = Path(source_path).resolve()
    
    for root, dirs, files in os.walk(source):
        # Remove ignored directories in-place
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            file_path = Path(root) / file
            ext = file_path.suffix.lower()
            
            if ext in PATTERNS:
                try:
                    content = file_path.read_text(encoding='utf-8')
                    matches = re.finditer(PATTERNS[ext], content, re.MULTILINE)
                    
                    for match in matches:
                        snippet = match.group(0).strip()
                        if len(snippet) > 8: # Skip trivial comments
                            relative_path = file_path.relative_to(source)
                            extracted_data.append({
                                "file": str(relative_path),
                                "language": ext[1:],
                                "content": snippet,
                                "type": "diagram" if "mermaid" in snippet.lower() else "comment"
                            })
                except Exception as e:
                    print(f"Warning: Could not read {file_path}: {e}")
                    
    return extracted_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="LaTeX Architect - Codebase Extraction Engine (v3.5)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--source", default=".", help="Directory to scan for documentation metadata")
    parser.add_argument("--output", default="docs/extracted_meta.json", help="Path to save the JSON extraction results")
    parser.add_argument("--ignore", nargs="+", default=list(IGNORE_DIRS), help="List of directory names to ignore")
    args = parser.parse_args()
    
    # Update global ignore dirs if provided
    if args.ignore:
        IGNORE_DIRS = set(args.ignore)
    
    print(f">>> Architect Scan Initialized: {args.source}")
    data = scan(args.source, ".")
    
    # Ensure output path is absolute or project-relative
    output_file = Path(args.output)
    if not output_file.is_absolute():
        # Resolve relative to project root (3 levels up from scripts/)
        output_file = Path(__file__).parents[3] / args.output
        
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        
    print(f">>> Extraction Complete. Found {len(data)} insights.")
    print(f">>> Saved to: {output_file.name}")
