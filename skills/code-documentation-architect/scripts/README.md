# Code Documentation Architect - Python Scripts

Fully functional automation scripts for the Code Documentation Architect skill. These scripts enable end-to-end code-documentation synchronization for any LaTeX-based project.

## Scripts

### 1. `extract_code_docs.py` - Extract Annotations
**Purpose**: Scan source files and extract `@doc:*` annotations from docstrings.

```bash
# Basic extraction
python extract_code_docs.py --source-dir src/ --output docs/code_metadata.json

# Scan multiple languages
python extract_code_docs.py --source-dir src/ --lang python,javascript,java

# With validation
python extract_code_docs.py --source-dir src/ --validate
```

**Output**: JSON file containing extracted artifact metadata with all `@doc:*` tags.

**Supported Languages**: Python, JavaScript, TypeScript, Java, C++, Go, Rust, C#

---

### 2. `lint_docstrings.py` - Enforce Standards
**Purpose**: Validate that all docstrings follow the annotation protocol.

```bash
# Lint entire directory
python lint_docstrings.py --source-dir src/

# Strict mode (fail on unknown fields)
python lint_docstrings.py --source-dir src/ --strict

# Lint single file
python lint_docstrings.py --file src/module.py

# Output JSON report
python lint_docstrings.py --source-dir src/ --json lint_report.json
```

**Checks**:
- Required fields present (@doc:chapter, @doc:section, @doc:artifact_id, etc.)
- Valid artifact ID formats (REQ-001, CODE-002, etc.)
- Description length (1-3 sentences recommended)
- Priority values (HIGH, MEDIUM, LOW)
- Unknown fields (in strict mode)

---

### 3. `validate_mappings.py` - Check Code-Docs Consistency
**Purpose**: Cross-validate that code artifacts are properly referenced in LaTeX documentation.

```bash
# Check for broken references
python validate_mappings.py --metadata docs/code_metadata.json --latex-dir Chapters/

# Trace design artifacts to requirements
python validate_mappings.py --metadata docs/code_metadata.json --trace-to-requirements ARCH

# Save detailed report
python validate_mappings.py --metadata docs/code_metadata.json --output validation_report.json
```

**Identifies**:
- Orphaned code artifacts (documented in code, not referenced in LaTeX)
- Broken LaTeX references (referenced in LaTeX, not in code)
- Missing traceability between requirements and implementation
- Incomplete bidirectional mappings

---

### 4. `generate_tables.py` - Create LaTeX Tables
**Purpose**: Generate standardized LaTeX table source code from artifact metadata.

```bash
# Generate all tables
python generate_tables.py --metadata docs/code_metadata.json --output-dir media/tables/

# Generate specific tables
python generate_tables.py --metadata docs/code_metadata.json --by-type requirements,tests,api

# Combine into single file
python generate_tables.py --metadata docs/code_metadata.json --single-file
```

**Generated Tables**:
- Requirements matrix (REQ-* artifacts)
- Test case tables (TC-* artifacts)
- API reference (API-* artifacts)
- Performance metrics (PERF-*, METRIC-* artifacts)
- Code modules (CODE-* artifacts)
- Requirements traceability matrix
- Chapter summaries

---

### 5. `coverage_report.py` - Analyze Documentation Coverage
**Purpose**: Generate comprehensive documentation coverage analytics.

```bash
# Generate full report
python coverage_report.py --metadata docs/code_metadata.json --output coverage_report.json

# Show coverage breakdown
python coverage_report.py --metadata docs/code_metadata.json --by-chapter --by-type

# Generate HTML report
python coverage_report.py --metadata docs/code_metadata.json --html coverage.html
```

**Reports**:
- Overall coverage percentage
- Coverage by chapter
- Coverage by artifact type (REQ, CODE, API, TC, etc.)
- Coverage by component (if tagged)
- Documentation gaps (missing descriptions, examples, diagrams)
- Requirements traceability metrics
- Broken reference list

---

### 6. `bidirectional_sync.py` - Orchestrate Full Pipeline
**Purpose**: Orchestrate complete extraction → linting → validation → generation → coverage pipeline.

```bash
# Run complete sync pipeline
python bidirectional_sync.py --full-sync

# Run specific steps
python bidirectional_sync.py --extract --validate --generate

# Quick validation check
python bidirectional_sync.py --quick-check

# With custom paths
python bidirectional_sync.py --full-sync --source-dir src/ --latex-dir Chapters/ --output-dir docs/
```

**Pipeline Steps**:
1. Extract code annotations → `code_metadata.json`
2. Lint for compliance → `lint_report.json`
3. Validate mappings → `validation_report.json`
4. Generate LaTeX tables → `media/tables/`
5. Analyze coverage → `coverage_report.json`

---

## Configuration

### Config File (config.json)

```json
{
  "source_dir": "./src",
  "latex_dir": "./Chapters",
  "output_dir": "./docs",
  "media_dir": "./media",
  "languages": ["python", "javascript"]
}
```

Use with: `python bidirectional_sync.py --config config.json`

---

## Output Files

### Generated Reports

| File | Purpose |
| --- | --- |
| `docs/code_metadata.json` | Extracted artifact metadata |
| `docs/lint_report.json` | Linting issues and violations |
| `docs/validation_report.json` | Mapping validation results |
| `docs/coverage_report.json` | Coverage metrics and gaps |
| `docs/sync_results.json` | Pipeline execution summary |
| `media/tables/all_tables.tex` | LaTeX table definitions |
| `coverage.html` | Interactive HTML coverage report |

### LaTeX Table Files

```
media/tables/
├── requirements_table.tex
├── test_cases_table.tex
├── api_reference_table.tex
├── performance_table.tex
├── code_modules_table.tex
├── traceability_table.tex
└── all_tables.tex        # Combined file
```

---

## Usage Examples

### Example 1: First-time Setup on New Project

```bash
# 1. Add @doc:* annotations to all source files
# (See skill.md for annotation format)

# 2. Extract and validate
python extract_code_docs.py --source-dir src/ --validate

# 3. Lint for compliance
python lint_docstrings.py --source-dir src/ --json reports/lint.json

# 4. Generate LaTeX tables for documentation
python generate_tables.py --metadata docs/code_metadata.json --output-dir media/

# 5. Check coverage
python coverage_report.py --metadata docs/code_metadata.json --by-chapter
```

### Example 2: Pre-commit Hook

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
cd skills/code-documentation-architect/scripts/
python bidirectional_sync.py --quick-check
if [ $? -ne 0 ]; then
    echo "✗ Documentation validation failed. Run full sync to fix."
    exit 1
fi
```

### Example 3: CI/CD Integration

```yaml
# GitHub Actions example
- name: Validate Documentation
  run: |
    cd skills/code-documentation-architect/scripts/
    python bidirectional_sync.py --full-sync
    
- name: Check Coverage
  run: |
    cd skills/code-documentation-architect/scripts/
    python coverage_report.py --metadata docs/code_metadata.json
```

### Example 4: Generate Coverage Report

```bash
python coverage_report.py \
  --metadata docs/code_metadata.json \
  --output coverage.json \
  --html coverage.html
```

---

## Requirements

- Python 3.7+
- No external dependencies (uses only stdlib: json, re, argparse, pathlib, dataclasses)

## Installation

```bash
# No installation needed - scripts are ready to use
# Just ensure Python 3.7+ is available

cd skills/code-documentation-architect/scripts/
python extract_code_docs.py --help
```

---

## Troubleshooting

### "File not found" errors

- Paths are relative to script directory
- Use absolute paths with `--source-dir`, `--latex-dir`, `--output-dir`

### No artifacts extracted

- Check that source files contain `@doc:*` annotations in docstrings
- Verify language is supported (use `--lang python` to debug)
- Ensure docstrings follow format: `"""..."""` (Python) or `/** ... */` (JS/Java)

### Orphaned artifacts reported

- Artifact exists in code but not referenced in LaTeX files
- Add `\ref{<artifact_id>}` or mention the ID in LaTeX chapter
- Or remove `@doc:*` annotations if artifact shouldn't be documented

### Broken references reported

- LaTeX file references an artifact ID that doesn't exist in code
- Check for typos in artifact IDs
- Verify metadata was extracted from updated source files

---

## Customization

All scripts are designed to be extensible:

### Adding custom artifact types

Edit the prefix list in each script (e.g., `ARTIFACT_ID_PREFIXES` in `lint_docstrings.py`)

### Changing LaTeX format

Modify `generate_tables.py` to output different table formats (booktabs, tabulary, etc.)

### Custom validation rules

Extend `AnnotationValidator` in `extract_code_docs.py` or `DocstringLinter` in `lint_docstrings.py`

---

## License

These scripts are part of the Code Documentation Architect skill template and are provided as part of the LaTeX documentation workflow.
