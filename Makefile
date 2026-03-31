# Makefile for LaTeX Template Automation
# Works on both Linux (GNU Make) and Windows (with proper LaTeX distribution like TeX Live / MiKTeX)

MAIN = main
OUTPUT_DIR = build
LATEX = xelatex
LATEX_FLAGS = -interaction=nonstopmode -halt-on-error

.PHONY: all clean generate view preview isolate titlepage scan

SOURCE = .
TARGET = frontmatter/abstract.tex
OUTPUT = docs/preview
IGNORE = .git node_modules .gemini

.PHONY: all preview isolate titlepage scan sync doctor clean merge

all:
	@echo ">>> Building LaTeX Production PDF..."
	@mkdir -p logs examples
	@$(LATEX) $(LATEX_FLAGS) -output-directory=logs $(MAIN).tex
	@bibtex logs/$(MAIN) || true
	@$(LATEX) $(LATEX_FLAGS) -output-directory=logs $(MAIN).tex
	@$(LATEX) $(LATEX_FLAGS) -output-directory=logs $(MAIN).tex
	@mv logs/$(MAIN).pdf examples/
	@echo ">>> Build complete! Output → examples/$(MAIN).pdf"

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
	rm -f *.aux *.log *.out *.toc *.lof *.lot *.blg *.bbl $(MAIN).pdf
	rm -rf logs $(OUTPUT_DIR)

merge:
	@echo ">>> Merging PDF with external covers..."
	@python skills/latex-template-architect/scripts/pdf_merger.py \
		--main examples/$(MAIN).pdf \
		--front $(EXTERNAL_FRONT) \
		--back $(EXTERNAL_BACK) \
		--output examples/$(MAIN)_final.pdf
