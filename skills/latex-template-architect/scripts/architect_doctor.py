import os
import sys
import subprocess
from pathlib import Path
import argparse

# architect_doctor.py - v3.5 Strategic Diagnostic tool
# Get the project root dynamically (3 levels up from this script: skills/latex-template-architect/scripts/)
import shutil
import getpass

def check_latex(selected_engines=None, manual_path=None):
    print(">>> Checking LaTeX Engine...")
    
    # Defaults if none selected
    if not selected_engines:
        selected_engines = ["xelatex", "pdflatex", "lualatex"]
    
    found = False
    current_user = getpass.getuser()
    
    # Known common installation paths (dynamic user-level lookup)
    common_paths = [
        rf"C:\Users\{current_user}\AppData\Local\Programs\MiKTeX\miktex\bin\x64",
        r"C:\Program Files\MiKTeX\miktex\bin\x64",
        r"C:\texlive\2024\bin\windows",
        r"C:\texlive\2023\bin\windows",
    ]
    
    if manual_path:
        common_paths.insert(0, manual_path)

    for engine in selected_engines:
        # 1. Standard Python discovery (handles .exe automatically)
        engine_path = shutil.which(engine)
        
        # 2. Check known common paths if not in system PATH
        if not engine_path:
            for p in common_paths:
                test_path = Path(p) / f"{engine}.exe"
                if test_path.exists():
                    engine_path = str(test_path)
                    break

        if engine_path:
            print(f"[OK] FOUND: {engine} -> {engine_path}")
            found = True
        else:
            # 3. Fallback for some shell-based discovery
            try:
                subprocess.run([engine, "--version"], capture_output=True, shell=True, check=True)
                print(f"[OK] SHELL_FOUND: {engine}")
                found = True
            except (subprocess.CalledProcessError, FileNotFoundError):
                 print(f"[MISSING] {engine}")
                 
    if not found:
        print("\n[!] WARNING: No LaTeX engine found in system path.")
        print("    If 'xelatex' works in your terminal but fails here, ensure:")
        print(f"    - Your LaTeX bin folder is in your PATH.")
        print(f"    - Suggested common user path: {common_paths[0]}")
    return found

def check_assets():
    print("\n>>> Checking Assets & Logos...")
    logo_dir = ROOT_DIR / "assets"
    logos = ["PRCLogo.png", "header.png", "footer.png"] # Replace the PRCLogo.png with your college logo
    if not logo_dir.exists():
        print(f"[FAIL] DIRECTORY MISSING: {logo_dir}")
        return
    for logo in logos:
        if (logo_dir / logo).exists():
            print(f"[OK] {logo}")
            if logo=="PRCLogo.png":
                print(f"[WARN] Replace the {logo} with your college logo at {logo_dir}")
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
    parser.add_argument("--engine", nargs="+", help="Specific engine(s) to verify (e.g., xelatex pdflatex)")
    parser.add_argument("--path", help="Manual path to a LaTeX bin directory to check")
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
        check_latex(selected_engines=args.engine, manual_path=args.path)
    
    check_assets()
    check_cache()
    
    print("-" * 40)
    print("Health Check Complete.")
