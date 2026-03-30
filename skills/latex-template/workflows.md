# Intelligent Documentation Workflows (v3.0)

## Workflow 1: Intelligent Initiation (Scan & Map)

**Trigger:** "Analyze codebase" / "Initialize documentation for [Project Path]"

```markdown
1. ESCAPE & SCAN
   - Exit the skill directory to the parent project root.
   - Run `powershell .\skills\latex-template\scripts\scan_codebase.ps1`.
   - Read the generated `docs/extracted_meta.json`.

2. EXTRACT SEMANTICS
   - Parse `extracted_meta.json` for:
     - Docstrings (Logic)
     - Mermaid blocks (Diagrams)
     - TODOs/Notes (Meta)
   - Update `docs/analysis_cache.json` -> `extracted_items`.

3. MAP INTENT
   - Compare `extracted_items` against `document_structure.chapters`.
   - Generate `mapping_proposals` in `docs/analysis_cache.json`.
   - LOG: "Proposed mapping [X] items to [Y] chapters."

4. USER GATING
   - Present the mapping summary to the user.
   - Ask: "Should I proceed with synthesis or do you want to adjust the mappings?"
```

---

## Workflow 2: Semantic Synthesis (Generate LaTeX)

**Trigger:** "Generate intelligence" / "Synthesize accepted mappings"

```markdown
1. LOAD PROPOSALS
   - Read `docs/analysis_cache.json` -> `mapping_proposals` where status is "accepted".

2. GENERATE SNIPPETS
   - For each proposal, generate a `.tex` snippet in `chapters/generated/`.
   - Format: `\section{...} \begin{quote} ... \end{quote}` or `\begin{figure} ... \end{figure}`.

3. UPDATE CHAPTERS (NON-DESTRUCTIVE)
   - Do NOT overwrite user-managed chapter files.
   - Suggest `\input{chapters/generated/filename.tex}` locations in the terminal.
   - User is responsible for manual placement within root `.tex` files.

4. LOG LINEAGE
   - Update `last_updated` and `hash` in the cache for change tracking.
```

---

## Workflow 3: Retrospective Review (Gap Analysis)

**Trigger:** "Retrospect report" / "Perform gap analysis"

```markdown
1. AUDIT COVERAGE
   - List all `extracted_items` that have NO `mapping_proposal`.
   - List all `chapters` that have NO `extracted_items` mapped to them.

2. LOG INCONSISTENCIES
   - Populate `docs/analysis_cache.json` -> `retrospective_report.issues`.
   - Type: `redundancy` | `gap` | `unmapped_source` | `empty_chapter`.

3. SUGGEST IMPROVEMENTS
   - Propose 3-5 structural refinements (e.g., "Merge Chapter 7 into 8 based on low content density").
   - Present these as actionable items to the user.
```

---

## Workflow 4: Build & Render (Compile PDF + Mermaid)

**Trigger:** "Build PDF" / "Render diagrams"

```markdown
1. RENDER DIAGRAMS
   - Locate all `extracted_items` of type "diagram".
   - Generate/Update `.mmd` files in `docs/diagrams/`.
   - Run: `mmdc -i docs/diagrams/<name>.mmd -o assets/<name>.png`.

2. COMPILE LATEX
   - Use the root `Makefile` if present.
   - Or: `pdflatex -output-directory=logs main.tex`.
   - Move final `logs/main.pdf` to `examples/[PROJECT]/main.pdf`.

3. VERIFY ARTIFACTS
   - Check if PDF contains the rendered diagrams.
   - Report any missing cross-references or unresolved macros.
```
