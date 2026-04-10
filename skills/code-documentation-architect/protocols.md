# SDLC Protocols & Verification Checkpoints

> **NOTE**: This is a template document. Customize the chapter names and examples for your project.

This document defines the phase-by-phase protocols and verification checkpoints for the Code Documentation Architect workflow.

---

## 1. Requirements Phase Protocol

### 1.1 Artifact Creation

**When**: Requirements gathering & specification phase

**How**: Add `@doc:*` annotations to requirement objects or specification files

```python
# requirements/user_stories.py
"""
@doc:chapter: <Your Analysis Chapter>
@doc:section: Functional Requirements
@doc:artifact_id: REQ-001
@doc:title: <Feature or Requirement Name>
@doc:description: <What the system shall do>
@doc:requirement: <User-facing requirement statement>
@doc:acceptance_criteria:
  - <Criterion 1>
  - <Criterion 2>
  - <Criterion 3>
@doc:is_functional: TRUE
@doc:priority: HIGH
"""
```

### 1.2 Verification Checkpoint (REQ-VERIFY)

**When**: Before moving to design phase

**What to check**:
- [ ] All requirements have unique `REQ-*` or `USE-CASE-*` IDs
- [ ] Each requirement has acceptance criteria
- [ ] No duplicate requirement IDs
- [ ] All descriptions are <= 3 sentences
- [ ] Priority level assigned (HIGH/MEDIUM/LOW)

**Command**:
```bash
python scripts/lint_docstrings.py --phase requirements --check-duplicates
python scripts/validate_mappings.py --check-orphaned REQ
```

**Expected Output**:
```
✓ X REQ-* artifacts validated
✓ Y USE-CASE-* artifacts validated
✓ No duplicate IDs found
✓ All artifacts have acceptance criteria
```

---

## 2. Design Phase Protocol

### 2.1 Artifact Creation

**When**: Architecture & design specification phase

**How**: Annotate design documents or diagram descriptions

```python
# design/architecture.py
"""
@doc:chapter: <Your Design Chapter>
@doc:section: <Architecture or System Design>
@doc:artifact_id: ARCH-001
@doc:title: <Architecture Name or Pattern>
@doc:description: <High-level description of the architecture and key design decisions>
@doc:diagram_type: component
@doc:include_tikz: TRUE
@doc:priority: HIGH
"""
```

### 2.2 Verification Checkpoint (DESIGN-VERIFY)

**When**: After all design documents are complete

**What to check**:
- [ ] All architecture components have `ARCH-*` IDs
- [ ] All sequence flows have `SEQ-*` IDs
- [ ] All class structures have `CLASS-*` IDs
- [ ] Diagrams reference matching code/implementation
- [ ] Traceability: Each design artifact maps to ≥1 requirement
- [ ] No unmapped design elements

**Command**:
```bash
python scripts/validate_mappings.py --trace-to-requirements ARCH
python scripts/validate_mappings.py --trace-to-requirements SEQ
```

**Expected Output**:
```
✓ 5 ARCH-* artifacts validated
✓ ARCH-001 → REQ-001, REQ-002, REQ-003
✓ All design artifacts traceable to requirements
```

---

## 3. Implementation Phase Protocol

### 3.1 Artifact Creation

**When**: During development (parallel with coding)

**How**: Add structured docstrings to all modules, classes, and public methods

```python
# src/trimmer.py
"""
Module: Video Trimmer
@doc:chapter: System Implementation
@doc:section: Video Trimmer Module
@doc:subsection: Scene Detection Algorithm
@doc:artifact_id: CODE-001
@doc:title: Scene Detection Engine
@doc:description: Segments video into gameplay fragments using Bhattacharyya distance-based 
scene change detection.
@doc:language: python
@doc:key_functions: [VideoTrimmer, process, _compute_hist]
@doc:dependencies: [cv2, numpy]
@doc:algorithm_complexity: O(n) per frame
@doc:priority: HIGH
@doc:related_artifacts: [ARCH-001, PERF-001]
"""

class VideoTrimmer:
    """
    @doc:class_description: Segments video into gameplay fragments.
    @doc:public_methods: [__init__, process]
    """
    
    def process(self):
        """
        @doc:method_description: Main processing loop for scene detection.
        @doc:output: Scene boundaries with timestamps
        """
        pass
```

### 3.2 Verification Checkpoint (CODE-VERIFY)

**When**: Before code review / before merging to main

**What to check**:
- [ ] All modules have `CODE-*` IDs
- [ ] All public APIs have `API-*` or `CODE-*` documentation
- [ ] All functions/classes have descriptive docstrings
- [ ] Code traceability: each module maps to ≥1 design artifact
- [ ] Dependencies listed and documented
- [ ] Complexity annotations present for algorithms
- [ ] No "TODO: document this" comments remain

**Command**:
```bash
python scripts/lint_docstrings.py --phase implementation --enforce-strict
python scripts/validate_mappings.py --trace-to-design CODE
```

**Expected Output**:
```
✓ 18 CODE-* modules validated
✓ CODE-001 → ARCH-001 (design trace)
✓ All public methods documented
✓ No undocumented modules found
```

---

## 4. Testing Phase Protocol

### 4.1 Artifact Creation

**When**: Test case definition and implementation

**How**: Add `@doc:*` annotations to test files

```python
# tests/test_trimmer.py
"""
@doc:chapter: Testing
@doc:section: Functional Test Cases
@doc:artifact_id: TC-001
@doc:test_name: Video Upload Validation
@doc:description: Verify uploaded videos meet size and codec requirements
@doc:preconditions: System is running, user is logged in
@doc:test_steps:
  - Click "Upload Video"
  - Select video file
  - Click "Start Upload"
@doc:expected_result: Video processing begins, progress bar visible
@doc:pass_criteria: Processing starts within 3 seconds
@doc:related_artifacts: [REQ-001]
"""

def test_video_upload_validation():
    pass
```

### 4.2 Verification Checkpoint (TEST-VERIFY)

**When**: After all test cases are written

**What to check**:
- [ ] All test cases have unique `TC-*` or `TEST-SUITE-*` IDs
- [ ] Test traceability: each test maps to ≥1 requirement
- [ ] Each requirement has ≥1 test case
- [ ] All test steps are clear and reproducible
- [ ] Pass/fail criteria are objective and measurable
- [ ] Test coverage ≥ 80% of codebase
- [ ] Acceptance criteria from requirements are tested

**Command**:
```bash
python scripts/validate_mappings.py --trace-to-requirements TC
python scripts/generate_tables.py --generate traceability_matrix
```

**Expected Output**:
```
✓ 32 TC-* test cases validated
✓ 100% of REQ-* covered by tests
✓ All test cases traceable to requirements
✓ Traceability matrix generated: docs/traceability_matrix.json
```

---

## 5. Verification & Validation Phase Protocol

### 5.1 Artifact Creation

**When**: Test execution, metrics collection, and results analysis

**How**: Log metrics and performance data with `@doc:*` annotations

```json
{
  "doc:chapter": "Results",
  "doc:section": "Performance Metrics",
  "doc:artifact_id": "PERF-001",
  "doc:metric_name": "End-to-End Latency",
  "doc:metric_value": "17.0",
  "doc:metric_unit": "milliseconds",
  "doc:metric_threshold": "< 30 ms",
  "doc:metric_status": "PASS",
  "doc:related_artifacts": ["CODE-002", "TC-015"]
}
```

### 5.2 Verification Checkpoint (RESULTS-VERIFY)

**When**: After all testing and metrics collection complete

**What to check**:
- [ ] All test cases executed and results recorded
- [ ] All performance metrics documented with `PERF-*` IDs
- [ ] Metrics compared against defined thresholds
- [ ] Coverage reports generate and linked
- [ ] All test results traceable back to requirements
- [ ] Pass/fail summary completed
- [ ] Deviations from requirements documented

**Command**:
```bash
python scripts/validate_mappings.py --full-coverage-report
python scripts/generate_tables.py --generate performance_summary
```

**Expected Output**:
```
✓ 32 tests executed
✓ 8 PERF-* metrics recorded
✓ 100% of tests passed
✓ Coverage: 96% of modules
✓ Performance summary generated: docs/performance_summary.json
```

---

## 6. Bidirectional Sync Protocol

### 6.1 Synchronization Workflow

**When**: Before PDF generation, after significant changes

**How**: Run full extraction → validation → sync pipeline

```bash
# Step 1: Extract all @doc:* annotations from code
make extract
# Output: docs/code_metadata.json

# Step 2: Validate all mappings and cross-references
make validate
# Output: docs/mapping_graph.json, validation_report.log

# Step 3: Generate LaTeX snippets and update .tex files
make generate
# Output: Updated ch3_system_analysis.tex, ch6_system_implementation.tex, etc.

# Step 4: Full synchronization report
make report
# Output: docs/coverage_report.json
```

### 6.2 Sync Verification

**Checklist**:
- [ ] `code_metadata.json` contains all extracted artifacts
- [ ] `mapping_graph.json` shows all bidirectional links
- [ ] No E001 (duplicate ID) errors
- [ ] No E002 (chapter mismatch) errors
- [ ] No E003 (missing required field) errors
- [ ] No E004 (invalid ID format) errors
- [ ] W001 warnings < 5 (orphaned code artifacts)
- [ ] W002 warnings < 5 (orphaned LaTeX references)
- [ ] All .tex files updated without corruption

---

## 7. Quality Gates

### 7.1 Pre-Commit Gate

**Runs**: Before each commit to repository

```bash
#!/bin/bash
make lint || exit 1
make extract || exit 1
make validate --strict || exit 1
```

**Fail Conditions**:
- Any E001-E004 errors
- > 5 W001/W002 warnings
- Docstring format violations
- Invalid artifact ID format

### 7.2 Pre-Review Gate

**Runs**: Before merge request/pull request

```bash
make lint --strict
make validate --full-coverage-report
make generate
```

**Fail Conditions**:
- Code coverage < 95%
- Any orphaned artifacts
- No traceability to requirements
- Missing test cases for new code

### 7.3 Pre-Build Gate

**Runs**: Before PDF generation

```bash
make sync
make report
```

**Fail Conditions**:
- Validation errors present
- Coverage report incomplete
- Broken cross-references
- Missing diagram files

---

## 8. Rollback & Correction Protocol

**If extraction fails**:
```bash
# 1. Check for syntax errors in docstrings
make lint --verbose

# 2. Fix errors in source files
# (edit offending docstrings)

# 3. Re-extract
make extract --force
```

**If LaTeX generation fails**:
```bash
# 1. Check mapping errors
python scripts/validate_mappings.py --verbose

# 2. Fix mapping issues in rules.md or source annotations
# 3. Re-generate
make generate --force
```

**If PDF build fails**:
```bash
# 1. Check LaTeX errors
cat main.log | grep "Error"

# 2. Review recently updated .tex files
# 3. Run full sync again
make sync --force

# 4. Force rebuild
latexmk -gg -pdf main.tex
```

---

## 9. Documentation Maintenance Schedule

| Frequency | Task | Command | Owner |
| :--- | :--- | :--- | :--- |
| Per Commit | Lint docstrings | `make lint` | Developer |
| Weekly | Validate mappings | `make validate` | Tech Lead |
| Before Release | Full sync & report | `make sync && make report` | QA Lead |
| Monthly | Coverage audit | `python scripts/coverage_report.py` | Documentation Owner |

---

## 10. Escalation & Support

**Issue**: Duplicate artifact ID found

- **Action 1**: Check `docs/code_metadata.json` for both occurrences
- **Action 2**: Determine which is authoritative (older or more referenced)
- **Action 3**: Rename other artifact ID
- **Action 4**: Re-run `make extract && make validate`

**Issue**: Chapter mismatch (CODE-* listed in chapter 5 instead of 6)

- **Action 1**: Review source file annotation
- **Action 2**: Verify `@doc:chapter` is correct
- **Action 3**: If incorrect, update annotation; if correct, check rule mismatch
- **Action 4**: Document any special cases in `rules.md`

**Issue**: Orphaned code artifact (not referenced in LaTeX)

- **Action 1**: Check if artifact is still relevant
- **Action 2**: If yes, add reference in appropriate chapter (.tex file)
- **Action 3**: If no, mark as deprecated or remove from source
- **Action 4**: Re-run validation

