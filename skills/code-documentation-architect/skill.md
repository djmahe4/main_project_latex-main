---
name: code-documentation-architect
mode: reusable
version: "2.0"
version_info: "Generic template - customize for your project"
dependencies: ["latex-template-architect"]  # Update to match your project's template skill name
---

# Code Documentation Architect (v1.0)
## SDLC Integration & LaTeX Mapping Protocol

> [!IMPORTANT]
> This skill defines the protocol for capturing, structuring, and mapping code artifacts to your LaTeX documentation workspace. All code documentation MUST comply with the mapping standards defined in this skill to ensure seamless integration with `latex-template-architect`.
>
> **Note**: This is a template skill. Customize the chapters, artifact types, and examples to match your project's structure.

---

## 1. Overview

The **Code Documentation Architect** bridges software development lifecycle (SDLC) artifacts—source code, design patterns, API specifications, and test cases—with the LaTeX documentation system. It ensures that technical documentation remains synchronized with the codebase and can be automatically extracted, transformed, and rendered into professional PDF documentation.

### Core Objectives
- Extract code metadata from source files in any language.
- Enforce consistent documentation protocols across the SDLC.
- Enable bidirectional mapping between code artifacts and LaTeX chapters.
- Maintain documentation freshness through automated scanning and validation.

### Customization Points
Before using this skill, customize the following:
- **Project chapters**: Update chapter names and file names in Section 3
- **Artifact ID prefixes**: Define prefixes for your SDLC phases (Section 4.2)
- **Example domain**: Replace video/media examples with your project's domain
- **Directory structure**: Adapt the directory layout to your project structure

---

## 2. Documentation Requirements by SDLC Phase

### 2.1 Requirements Phase
**Artifacts**: User Stories, Use Cases, Functional Requirements

**Documentation Format**:
```python
"""
@doc:chapter: <Your System Analysis Chapter>
@doc:section: Functional Requirements
@doc:requirement_id: REQ-001
@doc:requirement: <Describe the user-facing requirement>
@doc:acceptance_criteria:
  - <Acceptance criterion 1>
  - <Acceptance criterion 2>
  - <Acceptance criterion 3>
"""
```

**Mapping Rule**:
- Extract `@doc:chapter` → Destination chapter in LaTeX
- Extract `@doc:requirement_id` & `@doc:requirement` → Table row in requirements table
- Acceptance criteria → Nested bullet list environment

**Output LaTeX**:
```latex
\subsection{Requirement REQ-001}
<User-facing requirement description>
\begin{itemize}
  \item <Acceptance criterion 1>
  \item <Acceptance criterion 2>
  \item <Acceptance criterion 3>
\end{itemize}
```

---

### 2.2 Design Phase
**Artifacts**: Architecture Diagrams, Class Diagrams, Sequence Diagrams, API Specifications

**Documentation Format**:
```python
"""
@doc:chapter: <Your System Design Chapter>
@doc:section: <Subsystem or Component Name>
@doc:diagram_type: sequence
@doc:diagram_id: SEQ-001
@doc:title: <Sequence Title>
@doc:description: <Describe the interaction flow>
@doc:include_graphviz: True
"""
```

**Mapping Rules**:
- Extract `@doc:diagram_id` → Label for Mermaid/TikZ diagram reference
- Extract `@doc:title` & `@doc:description` → Caption and explanatory text
- Store diagram source in `media/diagrams/<DIAGRAM_ID>.mmd`
- Generate reference: `\ref{fig:<diagram_id_lowercase>}`

**Output LaTeX**:
```latex
\begin{figure}[h]
    \centering
    \input{media/diagrams/<DIAGRAM_ID>-tikz}
    \caption{<Sequence or diagram description>}
    \label{fig:<diagram_id_lowercase>}
\end{figure}
```

---

### 2.3 Implementation Phase
**Artifacts**: Source Code Modules, API Endpoints, Configuration Files

**Documentation Format**:
```python
"""
Module: <module_name>.py
@doc:chapter: <Your Implementation Chapter>
@doc:section: <Module or System Component Name>
@doc:subsection: <Specific Algorithm or Feature>
@doc:code_snippet_id: CODE-001
@doc:language: python
@doc:description: <Description of what this module/class does>
@doc:key_functions: [ClassName, method1, method2]
@doc:algorithm_complexity: <O(n), O(n²), etc.>
"""

class MyClass:
    """
    @doc:class_description: <What this class is responsible for>
    @doc:public_methods: [__init__, method1, method2]
    """
    
    def method1(self):
        """
        @doc:method_description: <What this method does>
        @doc:output: <What the method returns or produces>
        """
        pass
```

**Mapping Rules**:
- Extract `@doc:*` annotations from docstrings
- Extract class/method signatures → Table of API reference
- Extract key algorithms → Pseudocode in LaTeX `lstlisting`
- Map to corresponding chapter via `@doc:chapter`

**Output LaTeX**:
```latex
\subsection{<Algorithm or Feature Name>}
<Description of what this algorithm/feature does>

\subsubsection{Class: <ClassName>}
<What this class is responsible for>

\begin{table}[h]
  \centering
  \begin{tabular}{|l|l|l|}
    \hline
    \textbf{Method} & \textbf{Parameters} & \textbf{Returns} \\
    \hline
    method1 & param1, param2 & ReturnType \\
    method2 & param3 & AnotherReturnType \\
    \hline
  \end{tabular}
\end{table}

\begin{lstlisting}[language=<Language>, caption={<Code Description>}]
<Source code snippet>
\end{lstlisting}
```

---

### 2.4 Testing Phase
**Artifacts**: Test Cases, Test Results, Coverage Reports

**Documentation Format**:
```python
"""
@doc:chapter: <Your Testing Chapter>
@doc:section: Functional Test Cases
@doc:test_case_id: TC-001
@doc:test_name: <Test Case Name>
@doc:description: <What is being tested and why>
@doc:preconditions: <System state before test execution>
@doc:steps:
  - <Step 1>
  - <Step 2>
  - <Step 3>
@doc:expected_result: <Expected behavior/outcome>
@doc:pass_criteria: <Criteria for success>
"""
```

**Mapping Rules**:
- Extract `@doc:test_case_id`, `@doc:test_name` → Table row in test case matrix
- Extract `@doc:steps`, `@doc:expected_result` → Step-by-step procedure
- Extract `@doc:pass_criteria` → Acceptance condition

**Output LaTeX**:
```latex
\begin{table}[h]
  \centering
  \begin{tabular}{|l|p{8cm}|l|}
    \hline
    \textbf{Test Case ID} & \textbf{Description} & \textbf{Pass Criteria} \\
    \hline
    TC-001 & <Test case description> & <Success criteria> \\
    \hline
  \end{tabular}
  \caption{Functional Test Cases}
\end{table}
```

---

### 2.5 Verification & Validation Phase
**Artifacts**: Metrics Reports, Coverage Data, Performance Benchmarks

**Documentation Format**:
```json
{
  "doc:chapter": "<Your Results/Verification Chapter>",
  "doc:section": "<Metric Category>",
  "metrics": {
    "doc:metric_id": "PERF-001",
    "doc:metric_name": "<Metric Name>",
    "doc:value": "<Measured Value>",
    "doc:unit": "<Unit of Measurement>",
    "doc:threshold": "<Target or Threshold>",
    "doc:status": "<PASS|FAIL>"
  }
}
```

**Mapping Rules**:
- Extract all metrics → LaTeX table rows
- Aggregate by category (`doc:section`)
- Generate bar graphs for key metrics using `pgfplots`

---

## 3. Directory Structure & File Organization

```
project-root/
├── Chapters/                          ← Customize chapter names to match your project
│   ├── ch1_introduction.tex
│   ├── ch2_analysis.tex               ← REQ-* and USE-CASE-* mappings
│   ├── ch3_design.tex                 ← ARCH-*, SEQ-*, CLASS-* mappings
│   ├── ch4_implementation.tex         ← CODE-*, API-* mappings
│   ├── ch5_testing.tex                ← TC-* mappings
│   ├── ch6_results.tex                ← PERF-*, METRIC-* mappings
│   └── ch7_conclusions.tex
├── skills/
│   ├── code-documentation-architect/
│   │   ├── skill.md                   (this file)
│   │   ├── rules.md                   (mapping rules & constraints)
│   │   ├── protocols.md               (SDLC protocols & checklists)
│   │   └── scripts/
│   │       ├── extract_code_docs.py   (extract @doc: annotations)
│   │       ├── validate_mappings.py   (verify bidirectional links)
│   │       ├── generate_tables.py     (create requirement/test tables)
│   │       └── lint_docstrings.py     (enforce docstring format)
│   └── latex-template-architect/
│       ├── skill.md
│       └── scripts/
├── docs/
│   ├── code_metadata.json             (extracted from annotations)
│   ├── mapping_graph.json             (artifact → chapter → section links)
│   └── coverage_report.json           (documentation coverage %)
└── media/
    ├── diagrams/
    │   ├── ARCH-001.mmd               (Mermaid source)
    │   ├── SEQ-001-tikz.tex           (TikZ source)
    │   └── ...
    └── results/
        ├── metrics/
        │   └── perf_001_latency.csv
        └── ...
```

---

## 4. Annotation Protocol

### 4.1 Docstring Annotation Format

All documentation-bearing artifacts MUST use this format:

```python
"""
@doc:chapter: <CHAPTER_NAME>
@doc:section: <SECTION_NAME>
@doc:subsection: <OPTIONAL_SUBSECTION>
@doc:artifact_id: <UNIQUE_ID>
@doc:title: <HUMAN_READABLE_TITLE>
@doc:description: <DETAILED_DESCRIPTION>
@doc:tags: [tag1, tag2, tag3]
@doc:priority: <HIGH|MEDIUM|LOW>
@doc:last_updated: <YYYY-MM-DD>
"""
```

### 4.2 Artifact ID Naming Convention

| Phase | Prefix | Example | Destination Chapter | **CUSTOMIZE** |
| :--- | :--- | :--- | :--- | :--- |
| Requirements | `REQ-`, `USE-CASE-` | `REQ-001`, `USE-CASE-001` | <Your Analysis Chapter> | Update prefix/chapter name |
| Design | `ARCH-`, `SEQ-`, `CLASS-` | `ARCH-001`, `SEQ-001` | <Your Design Chapter> | Update prefix/chapter name |
| Implementation | `CODE-`, `API-`, `CONFIG-` | `CODE-001`, `API-001` | <Your Implementation Chapter> | Update prefix/chapter name |
| Testing | `TC-`, `TEST-SUITE-` | `TC-001`, `TEST-SUITE-001` | <Your Testing Chapter> | Update prefix/chapter name |
| Verification | `PERF-`, `METRIC-`, `COVERAGE-` | `PERF-001`, `METRIC-001` | <Your Results Chapter> | Update prefix/chapter name |

---

## 5. Bidirectional Mapping Workflow

### Phase A: Code → Documentation (Extraction)
1. Scan source files for `@doc:*` annotations
2. Parse each annotation and extract metadata
3. Store results in `docs/code_metadata.json`
4. Generate LaTeX snippets and update corresponding `.tex` files

### Phase B: Documentation → Code (Validation)
1. Scan LaTeX chapters for references to code artifacts (e.g., `\ref{fig:ARCH-001}`)
2. Cross-check against extracted metadata
3. Report broken or orphaned references
4. Suggest missing documentation in the codebase

### Phase C: Bidirectional Sync
1. Run Phase A to extract latest code metadata
2. Run Phase B to validate LaTeX references
3. Generate a Mapping Graph (`docs/mapping_graph.json`)
4. Create a Coverage Report showing undocumented code vs. orphaned docs

---

## 6. Automation Commands

| Command | Script | Action |
| :--- | :--- | :--- |
| `make extract` | `extract_code_docs.py` | Parse source files and extract `@doc:*` annotations |
| `make validate` | `validate_mappings.py` | Cross-check code artifacts against LaTeX references |
| `make generate` | `generate_tables.py` | Create requirement/test case/metric tables in LaTeX |
| `make lint` | `lint_docstrings.py` | Enforce docstring format and annotation compliance |
| `make sync` | `bidirectional_sync.py` | Full extraction → validation → sync pipeline |
| `make report` | `coverage_report.py` | Generate documentation coverage and mapping reports |

---

## 7. Integration with latex-template-architect

The **Code Documentation Architect** complements `latex-template-architect` by:

1. **Pre-processing**: Extracts code metadata before LaTeX synthesis
2. **Semantic Mapping**: Provides structured artifact → chapter mappings
3. **Validation**: Ensures all code is documented and all docs reference real artifacts
4. **Live Updates**: Re-runs extraction on every commit (via pre-commit hook)

---

## 8. Quality Assurance Checklist

- [ ] All source files contain `@doc:*` annotations in docstrings
- [ ] All artifact IDs follow naming convention (REQ-, CODE-, TC-, etc.)
- [ ] All `@doc:chapter` values match actual chapter file names
- [ ] All LaTeX `\ref{}` commands reference valid artifact IDs
- [ ] No orphaned artifacts (code with no docs, or docs with no code)
- [ ] All diagrams have IDs and are referenced in text
- [ ] Coverage report shows 100% of code modules documented
- [ ] All test cases are linked to requirements via traceability matrix

---

## 9. Example: Complete SDLC Artifact Chain

**Code (Implementation Phase)**:
```python
# src/<your_module>.py
"""
@doc:chapter: <Your Implementation Chapter>
@doc:section: <Component or Module Name>
@doc:artifact_id: CODE-002
@doc:title: <Feature or Processing Component Name>
"""
class YourClass:
    """
    @doc:description: <What this class orchestrates or does>
    @doc:key_methods: [method1, method2, method3]
    """
    def method1(self, parameters):
        """
        @doc:method_id: CODE-002-M1
        @doc:description: <What this method does>
        """
        pass
```

**LaTeX (Implementation Chapter)**:
```latex
\section{<Component Name>}
\label{sec:<component_name>}

As shown in Listing \ref{lst:CODE-002}, the <component description>.

\begin{lstlisting}[language=<Language>, label=lst:CODE-002, caption={<Class Name>}]
class YourClass:
    def method1(self, parameters):
        # <Implementation details>
        pass
\end{lstlisting}
```

---

## 10. Version History

| Version | Date | Changes |
| :--- | :--- | :--- |
| 1.0 | 2026-04-08 | Initial SDLC mapping protocol and automation framework |

