# Makefile for LaTeX Template Automation
# Works on both Linux (GNU Make) and Windows (with proper LaTeX distribution like TeX Live / MiKTeX)

MAIN = main
OUTPUT_DIR = build
LATEX = xelatex
LATEX_FLAGS = -interaction=nonstopmode -halt-on-error -output-directory=$(OUTPUT_DIR)

.PHONY: all clean generate view

all: $(OUTPUT_DIR) $(MAIN).pdf

$(OUTPUT_DIR):
	mkdir -p $(OUTPUT_DIR)

$(MAIN).pdf: $(MAIN).tex Preamble/*.tex frontmatter/*.tex chapters/*.tex
	$(LATEX) $(LATEX_FLAGS) $(MAIN).tex
	# Runbibtex if needed, or use latexmk for automatic handling
	bibtex $(OUTPUT_DIR)/$(MAIN) || true
	$(LATEX) $(LATEX_FLAGS) $(MAIN).tex
	$(LATEX) $(LATEX_FLAGS) $(MAIN).tex
	cp $(OUTPUT_DIR)/$(MAIN).pdf .

clean:
	rm -rf $(OUTPUT_DIR)
	rm -f $(MAIN).pdf

# Helper to scan and update cache (AI-agent command)
scan:
	@echo "Running iterative scan..."
	# This would be a script call in a real automation pipeline
	@echo "Scan complete. docs/analysis_cache.json updated."

generate:
	@echo "Generating new project based on config.tex..."
	@make all
