# Mapping Rules & Constraints

> **NOTE**: This is a template document. Customize the chapter names, artifact types, and mapping patterns for your project.

This document defines the immutable mapping rules and structural constraints for the Code Documentation Architect skill.

---

## 1. Artifact ID Mapping Table

| Phase | Prefix | Example | Destination Chapter | LaTeX Section | Regex Pattern |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Requirements | `REQ` | `REQ-001` | <Your Analysis Chapter> | Functional Requirements | `^REQ-\d{3}$` |
| Requirements | `USE-CASE` | `USE-CASE-001` | <Your Analysis Chapter> | Use Cases | `^USE-CASE-\d{3}$` |
| Design | `ARCH` | `ARCH-001` | <Your Design Chapter> | System Architecture | `^ARCH-\d{3}$` |
| Design | `SEQ` | `SEQ-001` | <Your Design Chapter> | Sequence Diagrams | `^SEQ-\d{3}$` |
| Design | `CLASS` | `CLASS-001` | <Your Design Chapter> | Class Diagrams | `^CLASS-\d{3}$` |
| Implementation | `CODE` | `CODE-001` | <Your Implementation Chapter> | Code Modules | `^CODE-\d{3}$` |
| Implementation | `API` | `API-001` | <Your Implementation Chapter> | API Reference | `^API-\d{3}$` |
| Implementation | `CONFIG` | `CONFIG-001` | <Your Implementation Chapter> | Configuration | `^CONFIG-\d{3}$` |
| Testing | `TC` | `TC-001` | <Your Testing Chapter> | Functional Test Cases | `^TC-\d{3}$` |
| Testing | `TEST-SUITE` | `TEST-SUITE-001` | <Your Testing Chapter> | Test Suites | `^TEST-SUITE-\d{3}$` |
| Verification | `PERF` | `PERF-001` | <Your Results Chapter> | Performance Metrics | `^PERF-\d{3}$` |
| Verification | `METRIC` | `METRIC-001` | <Your Results Chapter> | System Metrics | `^METRIC-\d{3}$` |
| Verification | `COVERAGE` | `COVERAGE-001` | <Your Results Chapter> | Code Coverage | `^COVERAGE-\d{3}$` |

---

## 2. LaTeX Cross-Reference Generation

### 2.1 Figure Labels

```
Artifact ID    →  LaTeX Label      →  Reference Command
REQ-001        →  fig:req_001      →  \ref{fig:req_001}
ARCH-001       →  fig:arch_001     →  \ref{fig:arch_001}
SEQ-001        →  fig:seq_001      →  \ref{fig:seq_001}
CODE-001       →  lst:code_001     →  \ref{lst:code_001}
```

### 2.2 Table Labels

```
Artifact ID        →  LaTeX Label         →  Reference
REQ-* (table)      →  tab:requirements    →  \ref{tab:requirements}
TC-* (table)       →  tab:test_cases      →  \ref{tab:test_cases}
PERF-* (table)     →  tab:performance     →  \ref{tab:performance}
```

### 2.3 Section Labels

```
Artifact ID        →  LaTeX Label              →  Reference
ARCH-* (section)   →  sec:architecture_design →  \ref{sec:architecture_design}
CODE-* (section)   →  sec:code_modules        →  \ref{sec:code_modules}
```

---

## 3. Docstring Annotation Constraints

### 3.1 Required Fields

Every code artifact MUST include these `@doc:*` annotations:

```python
@doc:chapter           # REQUIRED: Destination chapter name (e.g., "System Design")
@doc:section           # REQUIRED: Section within chapter
@doc:artifact_id       # REQUIRED: Unique identifier (REQ-001, CODE-001, etc.)
@doc:title             # REQUIRED: Human-readable title
@doc:description       # REQUIRED: Detailed description (1-3 sentences)
```

### 3.2 Optional Fields

```python
@doc:subsection        # OPTIONAL: Nested subsection name
@doc:tags              # OPTIONAL: Comma-separated tags [tag1, tag2, tag3]
@doc:priority          # OPTIONAL: HIGH | MEDIUM | LOW
@doc:last_updated      # OPTIONAL: YYYY-MM-DD format
@doc:related_artifacts # OPTIONAL: List of related artifact IDs
@doc:author            # OPTIONAL: Primary maintainer or author
```

### 3.3 Phase-Specific Fields

#### Requirements Phase
```python
@doc:requirement           # The actual requirement statement
@doc:acceptance_criteria   # List of acceptance criteria
@doc:is_functional         # TRUE | FALSE (functional vs. non-functional)
```

#### Design Phase
```python
@doc:diagram_type          # sequence | class | activity | component | state
@doc:diagram_id            # Short ID for diagram (e.g., SEQ-001)
@doc:include_graphviz      # TRUE | FALSE (use Graphviz for rendering)
@doc:include_tikz          # TRUE | FALSE (use TikZ for rendering)
```

#### Implementation Phase
```python
@doc:language              # python | javascript | java | cpp | etc.
@doc:key_functions         # List of primary functions/classes
@doc:dependencies          # External libraries or modules
@doc:algorithm_complexity  # Big-O notation (e.g., O(n log n))
```

#### Testing Phase
```python
@doc:test_case_id          # Unique test identifier (TC-001)
@doc:test_name             # Short test name
@doc:preconditions         # System state before test
@doc:test_steps            # Step-by-step procedure
@doc:expected_result       # Expected outcome
@doc:pass_criteria         # Acceptance condition
```

#### Verification Phase
```python
@doc:metric_id             # Metric identifier (PERF-001)
@doc:metric_name           # Human-readable metric name
@doc:metric_value          # Measured value
@doc:metric_unit           # Unit (ms, %, bytes, etc.)
@doc:metric_threshold      # Target or acceptable range
@doc:metric_status         # PASS | FAIL | WARN
```

---

## 4. File Pattern Constraints

### 4.1 Source Code Files

**Pattern**: `src/**/*.py` or `src/**/*.js`

**Constraint**:
- Module-level docstring MUST contain `@doc:*` annotations
- Class docstrings MUST have `@doc:class_description` and `@doc:public_methods`
- Public methods MUST have docstrings with `@doc:method_description`

### 4.2 Configuration Files

**Pattern**: `config/**/*.json` or `config/**/*.yaml`

**Constraint**:
- Top-level comment block MUST include `@doc:*` annotations
- For JSON: Use JavaScript comment blocks `/* */` above JSON
- For YAML: Use YAML comments `#` with `@doc:*` tags

### 4.3 Test Files

**Pattern**: `tests/**/*.py` or `tests/**/*.js`

**Constraint**:
- Each test function MUST have a docstring with `@doc:test_case_id`
- Test class MUST have `@doc:test_suite_id` annotation

---

## 5. Chapter Destination Rules

### 5.1 Ch. 3 System Analysis (ch3_system_analysis.tex)

**Allowed Artifact Prefixes**: `REQ-*`, `USE-CASE-*`

**Auto-generated Sections**:
- Functional Requirements (table)
- Non-Functional Requirements (table)
- Use Cases (list)
- System Constraints (list)

### 5.2 Ch. 5 System Design (ch5_system_design.tex)

**Allowed Artifact Prefixes**: `ARCH-*`, `SEQ-*`, `CLASS-*`

**Auto-generated Sections**:
- System Architecture (diagrams)
- Sequence Diagrams (figures)
- Class Diagrams (figures)
- Component Architecture (section)

### 5.3 Ch. 6 Implementation (ch6_system_implementation.tex)

**Allowed Artifact Prefixes**: `CODE-*`, `API-*`, `CONFIG-*`

**Auto-generated Sections**:
- Code Modules (listings)
- API Reference (table)
- Configuration (code blocks)

### 5.4 Ch. 7 Testing (ch7_testing.tex)

**Allowed Artifact Prefixes**: `TC-*`, `TEST-SUITE-*`

**Auto-generated Sections**:
- Test Case Matrix (table)
- Test Procedures (detailed steps)
- Test Coverage (metrics)

### 5.5 Ch. 8 Results (ch8_results.tex)

**Allowed Artifact Prefixes**: `PERF-*`, `METRIC-*`, `COVERAGE-*`

**Auto-generated Sections**:
- Performance Metrics (table + graphs)
- Build Statistics (table)
- Coverage Report (charts)

---

## 6. Validation Rules

### 6.1 Artifact ID Uniqueness

**Rule**: Each artifact ID MUST be globally unique across the codebase.

**Violation**: 
```
ERROR: Duplicate artifact ID CODE-001 found in:
  - src/trimmer.py (line 42)
  - src/processor.py (line 18)
```

### 6.2 Chapter-Artifact Compatibility

**Rule**: Artifact prefix MUST match destination chapter.

**Violation**:
```
ERROR: CODE-001 has @doc:chapter: "System Design" 
but CODE-* artifacts belong in Ch. 6 (Implementation)
```

### 6.3 Cross-reference Validity

**Rule**: All `\ref{}` commands in LaTeX MUST reference valid artifact IDs.

**Violation**:
```
ERROR: LaTeX reference \ref{fig:CODE-999} 
but CODE-999 not found in code_metadata.json
```

### 6.4 Bidirectional Completeness

**Rule**: Every code artifact MUST have a LaTeX reference, and vice versa.

**Orphaned Code**:
```
WARNING: CODE-005 extracted but never referenced in any .tex file
```

**Orphaned Docs**:
```
WARNING: \ref{lst:CODE-020} in ch6 but CODE-020 not found in source
```

---

## 7. Reserved Keywords

These artifact ID prefixes are reserved and MUST NOT be used for custom purposes:

```
REQ, USE-CASE, ARCH, SEQ, CLASS, CODE, API, CONFIG, TC, TEST-SUITE, PERF, METRIC, COVERAGE
```

Custom prefixes require approval and documentation in `skills.md`.

---

## 8. Metadata JSON Schema

### 8.1 code_metadata.json Structure

```json
{
  "extracted_at": "2026-04-08T14:32:00Z",
  "total_artifacts": 42,
  "artifacts": [
    {
      "artifact_id": "CODE-001",
      "phase": "implementation",
      "type": "code_module",
      "source_file": "src/trimmer.py",
      "line_number": 42,
      "title": "Video Trimmer",
      "description": "Scene detection module...",
      "chapter": "System Implementation",
      "section": "Video Trimmer Module",
      "tags": ["video", "processing", "detection"],
      "priority": "HIGH",
      "last_updated": "2026-04-08"
    }
  ]
}
```

### 8.2 mapping_graph.json Structure

```json
{
  "total_mappings": 42,
  "chapter_distribution": {
    "ch3_system_analysis": 12,
    "ch5_system_design": 8,
    "ch6_implementation": 18,
    "ch7_testing": 32,
    "ch8_results": 10
  },
  "bidirectional_links": [
    {
      "artifact_id": "CODE-001",
      "latex_ref": "\\ref{lst:code_001}",
      "chapter_file": "ch6_system_implementation.tex",
      "line_number": 145,
      "status": "VALID"
    }
  ]
}
```

---

## 9. Error Codes

| Code | Severity | Message | Resolution |
| :--- | :--- | :--- | :--- |
| E001 | ERROR | Duplicate artifact ID | Rename one to be unique |
| E002 | ERROR | Invalid chapter-artifact mapping | Move to correct chapter or change prefix |
| E003 | ERROR | Missing required @doc field | Add field to docstring |
| E004 | ERROR | Invalid artifact ID format | Use pattern `PREFIX-###` (e.g., CODE-001) |
| W001 | WARNING | Orphaned code artifact | Add LaTeX reference in appropriate chapter |
| W002 | WARNING | Orphaned LaTeX reference | Remove or create corresponding artifact |
| W003 | WARNING | Outdated @doc:last_updated field | Run `make lint` to auto-update |

---

## 10. Validation Checklist

Run before committing:

- [ ] All artifact IDs follow naming convention (`PREFIX-###`)
- [ ] No duplicate artifact IDs exist
- [ ] All `@doc:*` required fields are present
- [ ] All chapter destinations are valid
- [ ] All LaTeX `\ref{}` commands reference valid artifact IDs
- [ ] No orphaned code artifacts (unreferenced in LaTeX)
- [ ] No orphaned LaTeX references (not in code_metadata.json)
- [ ] All diagrams/figuresare properly labeled and captioned
- [ ] Code coverage ≥ 95%

