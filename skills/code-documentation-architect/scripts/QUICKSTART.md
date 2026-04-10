# Quick Start Guide - Code Documentation Architect Scripts

Get started with the automated documentation sync pipeline in 5 minutes.

## Prerequisites

- Python 3.7 or higher
- A LaTeX project with `Chapters/` directory
- Source code with `@doc:*` annotations (see [skill.md](../skill.md) for format)

## Step 1: Prepare Your Project

Annotate your source code with `@doc:*` tags. Example in Python:

```python
"""
@doc:chapter: System Implementation
@doc:section: Core Processing
@doc:artifact_id: CODE-001
@doc:title: Video Processing Engine
@doc:description: Main processing loop for video frame analysis.
"""
def process_video(input_path):
    pass
```

## Step 2: Configure Paths

Create `config.json` in this directory (or use defaults):

```json
{
  "source_dir": "./src",
  "latex_dir": "./Chapters",
  "output_dir": "./docs",
  "languages": ["python"]
}
```

Or use command-line flags when running scripts.

## Step 3: Run the Pipeline

### Option A: Complete Pipeline (Recommended)

```bash
# Run all steps: extract → lint → validate → generate → coverage
python bidirectional_sync.py --full-sync
```

This will:
1. Extract all `@doc:*` annotations
2. Check compliance with standards
3. Validate code-to-docs mappings
4. Generate LaTeX tables
5. Analyze coverage metrics

### Option B: Step by Step

```bash
# 1. Extract annotations
python extract_code_docs.py --source-dir src/ --validate

# 2. Check compliance
python lint_docstrings.py --source-dir src/ --json docs/lint.json

# 3. Validate mappings
python validate_mappings.py --metadata docs/code_metadata.json --latex-dir Chapters/

# 4. Generate LaTeX tables (include in your .tex chapters)
python generate_tables.py --metadata docs/code_metadata.json --single-file

# 5. View coverage report
python coverage_report.py --metadata docs/code_metadata.json
```

### Option C: Quick Check

```bash
# Just extract and validate (fast check)
python bidirectional_sync.py --quick-check
```

## Step 4: Use Generated Files

### LaTeX Tables

Generated tables are saved to `media/tables/all_tables.tex`:

```latex
% In your chapter file (e.g., Chapters/ch3_system_analysis.tex)
\section{Requirements}

% Include auto-generated requirement matrix
\input{../media/tables/all_tables.tex}
```

Tables include:
- Requirements matrix
- Test case tables
- API reference
- Performance metrics
- Traceability matrix

### Coverage Report

View human-readable coverage:

```bash
# Console output
python coverage_report.py --metadata docs/code_metadata.json

# HTML report
python coverage_report.py --metadata docs/code_metadata.json --html coverage.html
# Open coverage.html in a browser
```

View JSON report:

```bash
cat docs/coverage_report.json | python -m json.tool
```

## Step 5: Fix Issues

### Orphaned Artifacts

Code that's documented but not referenced in LaTeX:

```bash
python validate_mappings.py --metadata docs/code_metadata.json --latex-dir Chapters/
```

**Fix**: Add reference to LaTeX chapter or remove `@doc:*` annotations if not needed.

### Linting Errors

Documentation that doesn't comply with standards:

```bash
python lint_docstrings.py --source-dir src/ --json lint_report.json
cat lint_report.json | python -m json.tool
```

**Fix**: Add missing fields or correct format (see lint errors).

### Low Coverage

Identify what's not documented:

```bash
python coverage_report.py --metadata docs/code_metadata.json --show-gaps
```

**Fix**: Add `@doc:*` annotations to undocumented code.

---

## Common Workflows

### Adding New Feature

1. Write code with `@doc:*` annotations
2. Run: `python extract_code_docs.py --source-dir src/`
3. Check coverage: `python coverage_report.py --metadata docs/code_metadata.json`
4. Generate tables: `python generate_tables.py --metadata docs/code_metadata.json --single-file`
5. Include in LaTeX: `\input{../media/tables/all_tables.tex}`

### Pre-commit Validation

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
cd skills/code-documentation-architect/scripts/
python bidirectional_sync.py --quick-check
exit $?
```

Make executable: `chmod +x .git/hooks/pre-commit`

### CI/CD Pipeline

GitHub Actions example (`.github/workflows/docs.yml`):

```yaml
name: Validate Documentation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Run documentation sync
        run: |
          cd skills/code-documentation-architect/scripts/
          python bidirectional_sync.py --full-sync
```

### Using Makefile

```bash
# Extract (with default paths)
make extract

# Full pipeline with custom paths
make full-sync SRC_DIR=../other-project/code LATEX_DIR=../tex

# Generate coverage report
make coverage

# Clean generated files
make clean
```

---

## Troubleshooting

### "No artifacts found"

- Check source directory exists: `--source-dir src/`
- Verify language: `--lang python` (default)
- Check @doc: format in docstrings (requires triple quotes in Python)

### "Metadata file not found"

- Run extraction first: `python extract_code_docs.py ...`
- Check output path matches: `--metadata docs/code_metadata.json` (default)

### "LaTeX dir not found"

- Verify Chapters/ directory exists
- Or specify correct path: `--latex-dir ./my-chapters/`

### "Permission denied"

On Linux/Mac, make scripts executable:

```bash
chmod +x *.py
chmod +x Makefile
```

---

## Next Steps

1. **Customize** `skill.md` for your project (chapters, artifact types)
2. **Annotate** all source files with `@doc:*` tags
3. **Run** `python bidirectional_sync.py --full-sync`
4. **Include** generated LaTeX tables in your documentation
5. **Monitor** coverage with `python coverage_report.py`

For detailed documentation of each script, see [README.md](README.md).

---

## Support

For issues or questions:

1. Check [README.md](README.md) for detailed script documentation
2. Review [../skill.md](../skill.md) for annotation protocol
3. Look at [../protocols.md](../protocols.md) for SDLC workflows
4. Customize [../customization.md](../customization.md) for your project
