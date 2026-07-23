import os
import sys
import argparse
import subprocess
import re
import json
from pathlib import Path

# latex_studio.py - Surgical Build & Preview Manager (v3.6)

PREVIEW_INJECTION = r"\input{Preamble/preview.tex}"

class LatexValidator:
    """Pre-build diagnostic layer for LaTeX templates."""
    
    SUGGESTIONS = {
        "missing_file": "Verify path exists. Refs: https://en.wikibooks.org/wiki/LaTeX/Importing_Graphics",
        "placeholder": "Replace with actual value in config.tex or mapping_proposals.json.",
        "syntax_env": "Missing \\end for \\begin. Refs: https://www.overleaf.com/learn/latex/Errors",
        "syntax_brace": "Unclosed brace '{'. Check grouping."
    }

    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.errors = [] # List of tuples (file, line, type, msg)
        self.visited = set()
        self.virtual_files = {} # path -> updated_content
        self.mapping = self._load_mappings()

    def _load_mappings(self):
        """Loads mapping proposals for auto-fixing placeholders."""
        m_path = self.root_dir / "docs/mapping_proposals.json"
        if m_path.exists():
            with open(m_path, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    print("WARNING: Corrupt mapping_proposals.json. Skipping auto-fix.")
        return {}

    def _auto_fix(self, content, file_path):
        """Attempts to resolve placeholders in-memory."""
        updated = content
        # Match [var_name]
        placeholders = re.findall(r'\[([a-zA-Z0-9_ -]{2,})\]', content)
        for p in placeholders:
            if p in self.mapping:
                val = str(self.mapping[p])
                print(f"  [AUTO-FIX] Resolving [{p}] -> {val} in {file_path.name}")
                updated = updated.replace(f"[{p}]", val)
        return updated

    def validate_recursive(self, file_path):
        """Scan file and follow \input/\include recursively."""
        f_path = Path(file_path).resolve()
        if f_path in self.visited or not f_path.exists():
            return
        
        self.visited.add(f_path)
        try:
            content = f_path.read_text(encoding='utf-8')
        except Exception as e:
            self.errors.append((f_path, 0, "missing_file", f"Cannot read: {e}"))
            return
            
        # 1. Syntax Check (Basic)
        lines = content.splitlines()
        for i, line in enumerate(lines):
            # Simple brace balance (ignores comments for brevity)
            if "%" in line:
                line = line.split("%")[0]
            if line.count('{') > line.count('}'):
                self.errors.append((f_path, i+1, "syntax_brace", "Detected unclosed '{'."))
            
            # Placeholders
            if "[" in line and "]" in line:
                matches = re.finditer(r'\[([a-zA-Z0-9_ -]{3,})\]', line)
                for m in matches:
                    p = m.group(1)
                    if p in self.mapping:
                        continue # Will be fixed in memory
                    self.errors.append((f_path, i+1, "placeholder", f"Unresolved variable: [{p}]"))

        # Environment balance (Global for file)
        begins = re.findall(r'\\begin\{([^}]*)\}', content)
        ends = re.findall(r'\\end\{([^}]*)\}', content)
        if len(begins) != len(ends):
            self.errors.append((f_path, 0, "syntax_env", f"Mismatched environments: {len(begins)} begins vs {len(ends)} ends."))

        # 2. Path Check & Recursion
        paths = re.finditer(r'\\(?:input|include|includegraphics|addbibresource|bibliography)\{([^}]*)\}', content)
        for m in paths:
            path_str = m.group(1)
            search_path = Path(path_str)
            
            # Auto-suffix for \input or \include
            if not search_path.suffix and "graphics" not in m.group(0) and "bib" not in m.group(0):
                search_path = search_path.with_suffix(".tex")
            
            # Resolve
            resolved = f_path.parent / search_path
            if not resolved.exists():
                resolved = self.root_dir / search_path
            
            if not resolved.exists():
                self.errors.append((f_path, 0, "missing_file", f"Missing dependency: {path_str}"))
            elif resolved.suffix == ".tex":
                self.validate_recursive(resolved)

        # 3. Apply memory fixes
        self.virtual_files[str(f_path)] = self._auto_fix(content, f_path)

    def report(self, fail_on_error=True):
        """Prints a comprehensive diagnostic report."""
        if not self.errors:
            print("\n>>> PREPROCESSING: No critical errors found.")
            return True
        
        print("\n" + "!"*60)
        print("DIAGNOSTIC REPORT - Preprocessing Check")
        print("!"*60)
        
        # Group errors by file
        grouped = {}
        for f, line, etype, msg in self.errors:
            if f not in grouped: grouped[f] = []
            grouped[f].append((line, etype, msg))
            
        for f, errs in grouped.items():
            print(f"\n[{f.name}]")
            for line, etype, msg in errs:
                loc = f"L{line}" if line > 0 else "File"
                print(f"  - {loc} [{etype.upper()}]: {msg}")
                print(f"    Suggestion: {self.SUGGESTIONS.get(etype, 'Check syntax.')}")
        
        # Decide if fail
        critical = [e for e in self.errors if e[2] in ["missing_file", "placeholder", "syntax_brace", "syntax_env"]]
        if critical and fail_on_error:
            print(f"\nFAILED: {len(critical)} critical issues remain. Build aborted.")
            return False
        return True


def run_latex(main_file, engine=None):
    # Use specified engine or fallback to xelatex then pdflatex
    engines = [engine] if engine else ["xelatex", "pdflatex"]
    for eng in engines:
        try:
            print(f">>> Attempting build with {eng}...")
            cmd = [eng, "-interaction=nonstopmode", "-halt-on-error", main_file]
            subprocess.run(cmd, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            if engine:
                print(f"ERROR: Specified engine '{engine}' failed or not found.")
                break
            continue
    return False

def build_preview(main_tex, output_dir, engine=None, virtual_files=None):
    if virtual_files and str(main_tex) in virtual_files:
        content = virtual_files[str(main_tex)]
    else:
        content = Path(main_tex).read_text(encoding='utf-8')
        
    # Inject preview logic before \begin{document}
    new_content = content.replace(r"\begin{document}", f"{PREVIEW_INJECTION}\n\\begin{{document}}")
    
    temp_file = "main_preview_temp.tex"
    Path(temp_file).write_text(new_content, encoding='utf-8')
    
    if run_latex(temp_file, engine=engine):
        output_path = Path(output_dir) / "skeleton_preview.pdf"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        os.rename("main_preview_temp.pdf", output_path)
        print(f">>> Skeleton preview saved to {output_path}")
    else:
        print("ERROR: LaTeX build failed. Check your distribution (MikTeX/TeX Live).")
    
    # Cleanup
    for f in Path(".").glob("main_preview_temp.*"):
        f.unlink()

def build_isolate(target_file, output_dir, engine=None, root_dir=None):
    target = Path(target_file)
    basename = target.stem
    temp_file = f"isolate_{basename}.tex"
    
    # In isolation mode, we use config.tex from the root
    wrapper = rf"""
\documentclass[11pt,a4paper]{{report}}
\input{{Preamble/packages.tex}}
\input{{Preamble/config.tex}}
\input{{Preamble/fonts.tex}}
\input{{Preamble/pagestyle.tex}}
\input{{Preamble/sectionoptions.tex}}
\input{{Preamble/macro.tex}}
\begin{{document}}
\input{{{target_file}}}
\end{{document}}
"""
    Path(temp_file).write_text(wrapper, encoding='utf-8')
    
    if run_latex(temp_file, engine=engine):
        output_path = Path(output_dir) / f"{basename}_preview.pdf"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        os.rename(f"isolate_{basename}.pdf", output_path)
        print(f">>> Isolated artifact saved to {output_path}")
    else:
        print("ERROR: Isolation build failed.")
        
    for f in Path(".").glob(f"isolate_{basename}.*"):
        f.unlink()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="LaTeX Architect - Surgical Build & Preview Manager (v3.6)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("mode", choices=["preview", "isolate"], help="Build mode: Layout Preview or Isolated Chapter")
    parser.add_argument("--target", help="Target .tex file for isolation (required for 'isolate' mode)")
    parser.add_argument("--main", default="main.tex", help="Root LaTeX file to use for skeleton previews")
    parser.add_argument("--output", default="docs/preview", help="Output directory for generated PDFs")
    parser.add_argument("--engine", choices=["xelatex", "pdflatex"], help="Override default engine selection")
    parser.add_argument("--skip-validation", action="store_true", help="Skip pre-build file checks")
    parser.add_argument("--validate-only", action="store_true", help="Run preprocessing check and exit")
    args = parser.parse_args()
    
    # Standardize output path resolution (root relative)
    root_dir = Path(__file__).parents[3]
    output_dir = root_dir / args.output
    
    # Initialize Preprocessing Layer
    validator = LatexValidator(root_dir)
    target_to_validate = args.main if args.mode == "preview" else args.target
    
    if not args.skip_validation:
        print(f"\n>>> PREPROCESSING: Validating {target_to_validate}...")
        validator.validate_recursive(target_to_validate)
        if not validator.report(fail_on_error=not args.skip_validation):
            print(">>> BUILD ABORTED: Fix the errors above or use --skip-validation.")
            sys.exit(1)
            
    if args.validate_only:
        sys.exit(0)
    
    if args.mode == "preview":
        main_tex = Path(args.main)
        if not main_tex.is_absolute():
             main_tex = root_dir / args.main
        build_preview(main_tex, output_dir, engine=args.engine, virtual_files=validator.virtual_files)
    elif args.mode == "isolate":
        if not args.target:
            print("ERROR: --target is required for isolation mode.")
            sys.exit(1)
        build_isolate(args.target, output_dir, engine=args.engine, root_dir=root_dir)
