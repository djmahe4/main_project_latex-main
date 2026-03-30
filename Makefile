# Makefile for LaTeX Template Automation
# Works on both Linux (GNU Make) and Windows (with proper LaTeX distribution like TeX Live / MiKTeX)

MAIN = main
OUTPUT_DIR = build
LATEX = xelatex
LATEX_FLAGS = -interaction=nonstopmode -halt-on-error

.PHONY: all clean generate view preview isolate titlepage scan

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex Preamble/*.tex frontmatter/*.tex chapters/*.tex
SOURCE = .
TARGET = frontmatter/abstract.tex
OUTPUT = docs/preview
IGNORE = .git node_modules .gemini

.PHONY: all preview isolate titlepage scan sync doctor clean

all:
	@echo ">>> Building LaTeX Production PDF..."
	@xelatex -interaction=nonstopmode -halt-on-error $(MAIN).tex

preview:
	@echo ">>> Starting Skeleton Preview (Python Studio)..."
	@python skills/latex-template-architect/scripts/latex_studio.py preview --main $(MAIN).tex --output $(OUTPUT)

isolate:
	@echo ">>> Starting Surgical Build..."
	@python skills/latex-template-architect/scripts/latex_studio.py isolate --target $(TARGET) --output $(OUTPUT)

titlepage:
	@python skills/latex-template-architect/scripts/latex_studio.py isolate --target frontmatter/titlepage.tex --output $(OUTPUT)

scan:
	@echo ">>> Initializing Autonomous Scan..."
	@python skills/latex-template-architect/scripts/scan_codebase.py --source $(SOURCE) --ignore $(IGNORE)

sync:
	@echo ">>> Initializing Macro Synchronization..."
	@python skills/latex-template-architect/scripts/macro_sync.py

doctor:
	@echo ">>> Initializing System Health Check..."
	@python skills/latex-template-architect/scripts/architect_doctor.py

clean:
	powershell -Command "Remove-Item -Path *.aux, *.log, *.out, *.toc, *.lof, *.lot, *.blg, *.bbl, $(MAIN).pdf -ErrorAction SilentlyContinue; if (Test-Path $(OUTPUT_DIR)) { Remove-Item -Recurse -Force $(OUTPUT_DIR) }"
