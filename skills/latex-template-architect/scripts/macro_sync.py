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
    if not CONFIG_PATH.exists():
        print(f"ERROR: Missing {CONFIG_PATH.name}. Run 'make setup' first.")
        return
    
    config_content = CONFIG_PATH.read_text(encoding='utf-8')
    final_mappings = {}
    
    # Priority 1: User-Verified Mapping Proposals
    proposal_path = ROOT_DIR / "docs/mapping_proposals.json"
    if proposal_path.exists():
        print(f">>> Found Manual Proposals: {proposal_path.name}")
        with open(proposal_path, 'r', encoding='utf-8') as f:
            proposals = json.load(f)
            for macro, value in proposals.items():
                if value and value.strip():
                    final_mappings[macro] = value.strip()

    # Priority 2: Heuristic @tags from extracted_meta.json (Only fill gaps)
    if META_PATH.exists():
        print(f">>> Processing Heuristic Metadata: {META_PATH.name}")
        with open(META_PATH, 'r', encoding='utf-8') as f:
            meta_data = json.load(f)
            for item in meta_data:
                content = item.get('content', '')
                for tag, macro in MAPPING_RULES.items():
                    if macro not in final_mappings:
                        # Match @tag: value until end of line
                        match = re.search(fr"@{tag}:\s*([^\r\n]*)", content, re.IGNORECASE)
                        if match:
                            value = match.group(1).strip().rstrip('"""').rstrip("'''").strip()
                            if len(value) < 100: # Sanity check: no giant blocks
                                final_mappings[macro] = value

    # Apply all unique mappings
    updates_made = 0
    for macro, value in final_mappings.items():
        base_pattern = re.escape(f"\\newcommand{{\\{macro}}}")
        pattern = rf"({base_pattern}){{(.*?)}}"
        if re.search(pattern, config_content):
            print(f"   Mapping: {macro} -> {value}")
            config_content = re.sub(pattern, lambda m, v=value: f"{m.group(1)}{{{v}}}", config_content)
            updates_made += 1
                    
    if updates_made > 0:
        CONFIG_PATH.write_text(config_content, encoding='utf-8')
        print(f">>> Sync Complete! Applied {updates_made} updates to {CONFIG_PATH.name}.")
    else:
        print(">>> No new mapping proposals applied.")
                    
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
