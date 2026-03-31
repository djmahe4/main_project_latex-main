import argparse
import os
import re
import json
from pathlib import Path

# macro_sync.py - v3.5 Agentic Logic
# Maps extracted_meta.json data to \tpl* LaTeX macros in config.tex

# Get the project root dynamically (3 levels up from this script: skills/latex-template-architect/scripts/)
ROOT_DIR = Path(__file__).parents[3]
CONFIG_PATH = ROOT_DIR / "Preamble/config.tex"
META_PATH = ROOT_DIR / "docs/extracted_meta.json"

# Define mapping rules: meta_tag -> config_macro
MAPPING_RULES = {
    "title": "tplProjectTitle",
    "student": "tplStudentA",
    "reg": "tplRegA",
    "guide": "tplProjectGuide",
    "hod": "tplHODName"
}

def check_cache():
    print("\n>>> Checking Intelligence Layer...")
    cache_path = ROOT_DIR / "docs/analysis_cache.json"
    return cache_path.exists()

def check_assets():
    print("\n>>> Checking Assets & Logos...")
    logo_dir = ROOT_DIR / "assets"
    logos = ["PRCLogo.png", "header.png", "footer.png"]
    return all((logo_dir / logo).exists() for logo in logos)

def sync():
    if not CONFIG_PATH.exists() or not META_PATH.exists():
        print("ERROR: Missing config.tex or extracted_meta.json. Run 'make scan' first.")
        return
    
    with open(META_PATH, 'r', encoding='utf-8') as f:
        meta_data = json.load(f)
        
    config_content = CONFIG_PATH.read_text(encoding='utf-8')
    updates_made = 0
    
    # Simple heuristic: Look for @tag: value in extracted content
    for item in meta_data:
        content = item['content']
        for tag, macro in MAPPING_RULES.items():
            match = re.search(fr"@{tag}:\s*(.*)", content, re.IGNORECASE)
            if match:
                value = match.group(1).strip().rstrip('"""').rstrip("'''").strip()
                # Update the macro in config.tex
                pattern = fr"(\\newcommand{{\{macro}}}{{)(.*?)(\}})"
                replacement = f"\\1{value}\\3"
                
                if re.search(pattern, config_content):
                    print(f">>> Mapping found: @{tag} -> {macro} ({value})")
                    config_content = re.sub(pattern, replacement, config_content)
                    updates_made += 1
                    
    if updates_made > 0:
        CONFIG_PATH.write_text(config_content, encoding='utf-8')
        print(f">>> Sync Complete! Applied {updates_made} updates to {CONFIG_PATH.name}.")
    else:
        print(">>> No new mapping proposals found in metadata.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="LaTeX Architect - Autonomous Macro Synchronization (v3.5)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--config", default="Preamble/config.tex", help="Path to LaTeX preamble configuration file")
    parser.add_argument("--meta", default="docs/extracted_meta.json", help="Path to the extracted metadata JSON")
    args = parser.parse_args()
    
    # Resolve absolute paths relative to project root
    ROOT_DIR = Path(__file__).parents[3]
    CONFIG_PATH = ROOT_DIR / args.config
    META_PATH = ROOT_DIR / args.meta
    
    print(f">>> Initializing Macro Sync: {CONFIG_PATH.name}")
    sync()
