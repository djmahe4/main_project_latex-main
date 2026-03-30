import os
import sys
import subprocess
from pathlib import Path

# architect_doctor.py - v3.5 Strategic Diagnostic tool
# Get the project root dynamically (3 levels up from this script: skills/latex-template-architect/scripts/)
ROOT_DIR = Path(__file__).parents[3]

def check_latex():
    print(">>> Checking LaTeX Engine...")
    engines = ["xelatex", "pdflatex"]
    found = False
    for engine in engines:
        try:
            # Check version (subprocess-safe)
            subprocess.run([engine, "--version"], capture_output=True, check=True)
            print(f"[OK] FOUND: {engine}")
            found = True
        except (subprocess.CalledProcessError, FileNotFoundError):
             print(f"[MISSING] {engine}")
    if not found:
        print("WARNING: No LaTeX engine found in system path.")
    return found

def check_assets():
    print("\n>>> Checking Assets & Logos...")
    logo_dir = ROOT_DIR / "assets"
    logos = ["PRCLogo.png", "header.png", "footer.png"]
    if not logo_dir.exists():
        print(f"[FAIL] DIRECTORY MISSING: {logo_dir}")
        return
    for logo in logos:
        if (logo_dir / logo).exists():
            print(f"[OK] {logo}")
        else:
            print(f"[MISSING] {logo} - Expected in {logo_dir}")

def check_cache():
    print("\n>>> Checking Intelligence Layer...")
    cache_path = ROOT_DIR / "docs/analysis_cache.json"
    meta_path = ROOT_DIR / "docs/extracted_meta.json"
    
    if cache_path.exists():
        print(f"[OK] Cache Active: {cache_path}")
    else:
        print("[MISSING] analysis_cache.json")
        
    if meta_path.exists():
        print(f"[OK] Meta Data Active: {meta_path}")
    else:
        print("[INIT NEEDED] Run 'make scan' first.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="LaTeX Architect - Strategic Diagnostic Tool (v3.5)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--root", default=".", help="Project root directory for health checks")
    parser.add_argument("--skip-latex", action="store_true", help="Skip LaTeX engine verification")
    args = parser.parse_args()
    
    # Resolve absolute project root
    ROOT_DIR = Path(args.root).resolve()
    if not (ROOT_DIR / "Preamble").exists():
        # Fallback to dynamic resolution if running from inside skills/ scripts/
        ROOT_DIR = Path(__file__).parents[3]

    print("-" * 40)
    print("LaTeX Architect Doctor: System Health Check")
    print(f"Project Root: {ROOT_DIR}")
    print("-" * 40)
    
    if not args.skip_latex:
        check_latex()
    
    check_assets()
    check_cache()
    
    print("-" * 40)
    print("Health Check Complete.")
