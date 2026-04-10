# Project Customization Template

This document tailors the universal **Code Documentation Architect** skill to your specific project.

---

## 1. Project Context

Fill in your project details:

| Property | Value |
| :--- | :--- |
| **Project** | <Your Project Name & Description> |
| **Language** | <Your Language(s)> |
| **Documentation Backend** | LaTeX (PDF) / Markdown / HTML |
| **Target Audience** | <Academic / Technical / Business> |
| **Chapter Structure** | <Number of chapters and naming conventions> |

---

## 2. Project-Specific Artifact Mapping

Customize the universal skill artifact types and destinations for your project:

| Phase | Prefixes | Destination Chapters |
| :--- | :--- | :--- |
| Requirements | `REQ-*`, `USE-CASE-*` | <Your Chapter Name> |
| Design | `ARCH-*`, `SEQ-*`, `CLASS-*` | <Your Chapter Name> |
| Implementation | `CODE-*`, `API-*`, `CONFIG-*` | <Your Chapter Name> |
| Testing | `TC-*`, `TEST-SUITE-*` | <Your Chapter Name> |
| Verification | `PERF-*`, `METRIC-*`, `COVERAGE-*` | <Your Chapter Name> |

### Chapter File Names
```
Chapters/
├── <Chapter 1>
├── <Chapter 2>
├── <Chapter 3 - Maps to REQ-*, USE-CASE-*>
├── <Chapter 4>
├── <Chapter 5 - Maps to ARCH-*, SEQ-*, CLASS-*>
├── <Chapter 6 - Maps to CODE-*, API-*, CONFIG-*>
├── <Chapter 7 - Maps to TC-*, TEST-SUITE-*>
├── <Chapter 8 - Maps to PERF-*, METRIC-*, COVERAGE-*>
└── <Final Chapter>
```

---

## 3. Required `@doc:*` Annotation Fields

### For All Phases
```python
@doc:chapter           # Your project's chapter name
@doc:section           # Specific section name within the chapter
@doc:artifact_id       # REQ-001, CODE-001, TC-001, etc.
@doc:title             # Human-readable title
@doc:description       # 1-3 sentences describing the artifact
```

### Optional Project-Specific Enhancements
```python
@doc:component         # <Your Component Name> (e.g., MODULE_A, SERVICE_B)
@doc:related_diagrams  # List of diagram IDs from media/diagrams/
@doc:performance_impact # HIGH | MEDIUM | LOW (impact on your system)
@doc:tags              # Custom tags relevant to your project
```

---

## 4. Your Project Component Mapping

Optional metadata for organizing code by system component:

| Component | Modules | Example Artifacts |
| :--- | :--- | :--- |
| <Component 1> | <Your module paths> | <Example artifact IDs> |
| <Component 2> | <Your module paths> | <Example artifact IDs> |
| <Component 3> | <Your module paths> | <Example artifact IDs> |

---

## 5. Customization Checklist

Before using this skill on your project:

- [ ] Update chapter file names in Section 2
- [ ] Map artifact types to your chapter destinations
- [ ] Define your project's component structure (if applicable)
- [ ] Add any project-specific `@doc:*` annotation fields
- [ ] Update the regex patterns in `rules.md` if you're using different prefixes
- [ ] Test the skill with a sample artifact before applying to entire codebase

## 5. LaTeX Output Specifics

### Chapter 6 Auto-Generated Sections

When `make generate` runs, the following sections are created:

```latex
\section{Video Trimmer Module}  % CODE-001
\section{Object Detection System}  % CODE-002, CODE-003
\section{Pitch Registration Engine}  % CODE-004
\section{Multi-Object Tracking}  % CODE-005
\section{Re-Identification (ReID) Layer}  % CODE-006
\section{Tactical RAG Agent}  % CODE-007
\section{API Reference}  % API-*
```

### Code Listings Format in LaTeX

```latex
\begin{lstlisting}[language=Python, 
                   label=lst:CODE-001, 
                   caption={Bhattacharyya Distance Scene Detection}]
def _compute_hist(self, frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    ...
\end{lstlisting}

See Listing \ref{lst:CODE-001} for the implementation details.
```

---

## 6. Performance Metrics for FootyDJ

Specific `@doc:*` fields for Ch. 8 Results:

```python
"""
@doc:chapter: Results
@doc:section: Performance Metrics
@doc:artifact_id: PERF-001
@doc:metric_name: YOLOv8 Inference Latency
@doc:metric_value: 8.6
@doc:metric_unit: ms
@doc:metric_threshold: < 15 ms (target for 30 FPS)
@doc:metric_status: PASS
@doc:hardware_config: NVIDIA RTX 3060
@doc:dataset: SoccerNet-v3 Test Split
"""
```

---

## 7. Testing Protocol for FootyDJ

All test cases reference:
- Input: Video fragments, broadcast scenes
- Expected: Accurate detection, tracking, tactical analysis
- Dataset: SoccerNet-v3 (90 matches)

```python
"""
@doc:chapter: Testing
@doc:section: Functional Test Cases
@doc:artifact_id: TC-001
@doc:test_name: Video Upload Validation
@doc:preconditions: System running, sample video available
@doc:test_steps:
  - Upload a 10-minute football match clip (MP4)
  - Verify scene detection triggers
  - Check player/ball tracking output
@doc:expected_result: Frame-by-frame JSON output generated
@doc:pass_criteria: < 50ms per frame latency
@doc:dataset_used: SoccerNet Premier League 2022-2023
"""
```

---

## 8. Integration with FootyDJ Architecture

```
FootyDJ Source Code (Python)
    ↓ Extract @doc:* annotations
    ↓ extract_code_docs.py
Code Metadata (JSON)
    ↓ Validate mappings
    ↓ validate_mappings.py
LaTeX Chapters (ch6, ch8, etc.)
    ↓ Generate listings, tables
    ↓ generate_tables.py
main.pdf (69 pages)
    ↓ Cross-reference resolution
    ↓ latexmk -pdf main.tex
Final Report (Ch.6: Implementation, Ch.8: Results)
```

---

## 9. Quality Standards for FootyDJ

### Code Documentation Requirements
- [ ] All modules (VISION, TRACKING, RAG, TACTICAL AI, INFRA) documented
- [ ] Artifact IDs follow naming: `CODE-###`, `API-###`, `PERF-###`, etc.
- [ ] All LaTeX `\ref{}` commands reference valid artifact IDs
- [ ] No orphaned code (unreferenced in docs)
- [ ] No orphaned docs (references non-existent code)
- [ ] All diagrams (TikZ in ch5, results in ch8) have valid IDs
- [ ] Coverage ≥ 95% (at least 19/20 modules documented)

### LaTeX Compilation Requirements
- [ ] All chapters compile without errors
- [ ] Page numbering consistent
- [ ] All cross-references resolved
- [ ] Heading alignment: chapters centered, subheadings left
- [ ] Images embedded in media/ directory
- [ ] Bibliography entries cross-linked

---

## 10. Automation Commands for FootyDJ

All commands run from project root:

```bash
# Extract code artifacts from src/
make extract
# → docs/code_metadata.json (FootyDJ components, modules, functions)

# Validate mappings
make validate
# → docs/mapping_graph.json
# → Checks all CODE-*, API-*, PERF-* references

# Generate LaTeX snippets
make generate
# → Updates Chapters/ch6_system_implementation.tex
# → Updates Chapters/ch8_results.tex
# → Creates listings and performance tables

# Full sync
make sync
# → extract + validate + generate in sequence

# Build final PDF
latexmk -pdf main.tex
# → main.pdf (71 pages with synchronized code + results)
```

---

## 11. Example: Complete FootyDJ Artifact Chain

### Step 1: Code (Implementation)
```python
# src/trimmer.py
"""
@doc:chapter: System Implementation
@doc:section: Video Trimmer Module
@doc:artifact_id: CODE-001
@doc:title: Scene Detection Engine
@doc:description: Segments video into gameplay fragments using Bhattacharyya distance.
@doc:language: python
@doc:footydj_component: VISION
@doc:performance_impact: HIGH
@doc:related_artifacts: [PERF-001, TC-015]
"""
```

### Step 2: Extraction
```bash
$ make extract
✓ Found CODE-001 in src/trimmer.py (line 42)
✓ Stored in docs/code_metadata.json
```

### Step 3: Generation
```bash
$ make generate
✓ Generated listing: Listing 6.1 (CODE-001)
✓ Updated ch6_system_implementation.tex
✓ Added cross-reference \ref{lst:code_001}
```

### Step 4: LaTeX Output (Ch. 6)
```latex
\section{Video Trimmer Module}
\label{sec:video_trimmer}

The scene detection engine (Listing \ref{lst:code_001}) segments video into gameplay fragments 
using Bhattacharyya distance-based scene change detection.

\begin{lstlisting}[language=Python, label=lst:code_001, caption={Scene Detection Implementation}]
def _compute_hist(self, frame):
    # Implementation...
\end{lstlisting}

\subsection{Performance Impact}
As measured in PERF-001, this module contributes 8.6ms to the per-frame latency.
```

---

## 12. Verification Checklist (FootyDJ-Specific)

Before finalizing the project report:

- [ ] All 5 core components (VISION, TRACKING, RAG, TACTICAL AI, INFRASTRUCTURE) have CODE-* artifacts
- [ ] Ch. 6 Implementation has ≥15 code listings
- [ ] Ch. 8 Results has ≥8 performance metrics (PERF-*)
- [ ] All test cases (Ch. 7) traceable to requirements (Ch. 3)
- [ ] No broken LaTeX cross-references (`\ref{}` warnings = 0)
- [ ] Page count: 69-75 pages (including front matter + appendices)
- [ ] Bibliography: ≥20 references properly formatted
- [ ] All images (TikZ diagrams, heatmaps, confusion matrices) rendered correctly

---

## 13. Maintenance & Updates

**When code changes**:
```bash
# After modifying src/trimmer.py or any module:
make extract
make validate
# → Verifies CODE-* IDs still valid
# → Updates docs/code_metadata.json
```

**When adding new test cases**:
```bash
# After writing tests/test_*.py:
make lint
make validate --strict
# → Ensures all TC-* IDs match new tests
```

**Before PDF compilation**:
```bash
# Final sync before latexmk:
make sync
# → Extract + Validate + Generate in one pass
latexmk -pdf main.tex
```

---

## 14. References

- **Generic Skill**: `skills/code-documentation-architect/skill.md`
- **Mapping Rules**: `skills/code-documentation-architect/rules.md`
- **SDLC Protocols**: `skills/code-documentation-architect/protocols.md`
- **LaTeX Skill**: `skills/latex-template-architect/skill.md`
- **Main Document**: `main.tex` → `main.pdf`

