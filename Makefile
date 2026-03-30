# Makefile for LaTeX Template Automation
# Works on both Linux (GNU Make) and Windows (with proper LaTeX distribution like TeX Live / MiKTeX)

MAIN = main
OUTPUT_DIR = build
LATEX = xelatex
LATEX_FLAGS = -interaction=nonstopmode -halt-on-error

.PHONY: all clean generate view preview isolate titlepage scan

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex Preamble/*.tex frontmatter/*.tex chapters/*.tex
	$(LATEX) $(LATEX_FLAGS) $(MAIN).tex
	# bibtex $(MAIN) || true # Run if needed
	$(LATEX) $(LATEX_FLAGS) $(MAIN).tex
	$(LATEX) $(LATEX_FLAGS) $(MAIN).tex

clean:
	powershell -Command "Remove-Item -Path *.aux, *.log, *.out, *.toc, *.lof, *.lot, *.blg, *.bbl, $(MAIN).pdf -ErrorAction SilentlyContinue; if (Test-Path $(OUTPUT_DIR)) { Remove-Item -Recurse -Force $(OUTPUT_DIR) }"

preview:
	@echo ">>> Starting Skeleton Preview (Python Studio)..."
	@python skills/latex-template-architect/scripts/latex_studio.py preview --main $(MAIN).tex --output docs/preview

isolate:
	@python skills/latex-template-architect/scripts/latex_studio.py isolate --target $(TARGET) --output docs/preview

titlepage:
	@python skills/latex-template-architect/scripts/latex_studio.py isolate --target frontmatter/titlepage.tex --output docs/preview

scan:
	@python skills/latex-template-architect/scripts/scan_codebase.py --source $(SOURCE)
