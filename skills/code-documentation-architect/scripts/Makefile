.PHONY: help extract lint validate generate coverage sync full-sync quick-check clean

SRC_DIR ?= ./src
LATEX_DIR ?= ./Chapters
OUTPUT_DIR ?= ./docs
MEDIA_DIR ?= ./media
LANG ?= python

help:
	@echo "Code Documentation Architect - Automation Commands"
	@echo ""
	@echo "Usage: make [command] [SRC_DIR=path] [LATEX_DIR=path] [OUTPUT_DIR=path] [LANG=python,javascript]"
	@echo ""
	@echo "Available commands:"
	@echo "  make extract         - Extract @doc:* annotations from source code"
	@echo "  make lint            - Lint docstrings for compliance"
	@echo "  make validate        - Validate code-to-docs mappings"
	@echo "  make generate        - Generate LaTeX tables from artifacts"
	@echo "  make coverage        - Analyze documentation coverage"
	@echo "  make sync            - Run extraction + validation (quick check)"
	@echo "  make full-sync       - Run complete pipeline (all steps)"
	@echo "  make clean           - Clean generated files"
	@echo ""
	@echo "Examples:"
	@echo "  make extract SRC_DIR=../my-project/src"
	@echo "  make full-sync SRC_DIR=src LATEX_DIR=Chapters"
	@echo "  make coverage LANG=python,javascript"

extract:
	@echo "Extracting code documentation from $(SRC_DIR)..."
	python extract_code_docs.py \
		--source-dir $(SRC_DIR) \
		--output $(OUTPUT_DIR)/code_metadata.json \
		--lang $(LANG) \
		--validate

lint:
	@echo "Linting docstrings for compliance..."
	python lint_docstrings.py \
		--source-dir $(SRC_DIR) \
		--json $(OUTPUT_DIR)/lint_report.json

validate:
	@echo "Validating code-to-documentation mappings..."
	python validate_mappings.py \
		--metadata $(OUTPUT_DIR)/code_metadata.json \
		--latex-dir $(LATEX_DIR) \
		--output $(OUTPUT_DIR)/validation_report.json

generate:
	@echo "Generating LaTeX tables..."
	@mkdir -p $(MEDIA_DIR)/tables
	python generate_tables.py \
		--metadata $(OUTPUT_DIR)/code_metadata.json \
		--output-dir $(MEDIA_DIR)/tables \
		--single-file

coverage:
	@echo "Analyzing documentation coverage..."
	python coverage_report.py \
		--metadata $(OUTPUT_DIR)/code_metadata.json \
		--output $(OUTPUT_DIR)/coverage_report.json \
		--by-chapter \
		--by-type

sync: extract validate
	@echo "✓ Quick sync complete (extract + validate)"

full-sync:
	@echo "Running complete documentation sync pipeline..."
	python bidirectional_sync.py --full-sync \
		--source-dir $(SRC_DIR) \
		--latex-dir $(LATEX_DIR) \
		--output-dir $(OUTPUT_DIR)

quick-check:
	@echo "Running quick validation check..."
	python bidirectional_sync.py --quick-check \
		--source-dir $(SRC_DIR) \
		--latex-dir $(LATEX_DIR)

clean:
	@echo "Cleaning generated files..."
	@rm -rf $(OUTPUT_DIR)/*.json
	@rm -rf $(MEDIA_DIR)/tables/*.tex
	@echo "✓ Clean complete"

.PHONY: help extract lint validate generate coverage sync full-sync quick-check clean
