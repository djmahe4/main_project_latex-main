import os
import sys
import argparse
import subprocess
from pathlib import Path

# latex_studio.py - Surgical Build & Preview Manager (v3.5)

PREVIEW_INJECTION = r"\input{Preamble/preview.tex}"

def run_latex(main_file):
    # Try xelatex then pdflatex
    for engine in ["xelatex", "pdflatex"]:
        try:
            print(f">>> Attempting build with {engine}...")
            cmd = [engine, "-interaction=nonstopmode", "-halt-on-error", main_file]
            subprocess.run(cmd, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    return False

def build_preview(main_tex, output_dir):
    content = Path(main_tex).read_text(encoding='utf-8')
    # Inject preview logic before \begin{document}
    new_content = content.replace(r"\begin{document}", f"{PREVIEW_INJECTION}\n\\begin{{document}}")
    
    temp_file = "main_preview_temp.tex"
    Path(temp_file).write_text(new_content, encoding='utf-8')
    
    if run_latex(temp_file):
        output_path = Path(output_dir) / "skeleton_preview.pdf"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        os.rename("main_preview_temp.pdf", output_path)
        print(f">>> Skeleton preview saved to {output_path}")
    else:
        print("ERROR: LaTeX build failed. Check your distribution (MikTeX/TeX Live).")
    
    # Cleanup
    for f in Path(".").glob("main_preview_temp.*"):
        f.unlink()

def build_isolate(target_file, output_dir):
    target = Path(target_file)
    basename = target.stem
    temp_file = f"isolate_{basename}.tex"
    
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
    
    if run_latex(temp_file):
        output_path = Path(output_dir) / f"{basename}_preview.pdf"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        os.rename(f"isolate_{basename}.pdf", output_path)
        print(f">>> Isolated artifact saved to {output_path}")
    else:
        print("ERROR: Isolation build failed.")
        
    for f in Path(".").glob(f"isolate_{basename}.*"):
        f.unlink()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["preview", "isolate"])
    parser.add_argument("--target", help="Target .tex file for isolation")
    parser.add_argument("--main", default="main.tex", help="Root LaTeX file")
    parser.add_argument("--output", default="docs/preview", help="Output directory")
    args = parser.parse_args()
    
    if args.mode == "preview":
        build_preview(args.main, args.output)
    elif args.mode == "isolate":
        if not args.target:
            print("ERROR: --target is required for isolation mode.")
            sys.exit(1)
        build_isolate(args.target, args.output)
