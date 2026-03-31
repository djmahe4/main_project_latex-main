## Workflow 1: Intelligent Initiation (Scan & Sync)

**Trigger:** "Analyze codebase" / "Initialize documentation for [Project Path]"

```markdown
1. ENVIRONMENT CHECK
   - Run `python skills/latex-template-architect/scripts/architect_doctor.py`.
   - Report any missing logos, engines, or caches. Use `--skip-latex` for CI environments.

2. ESCAPE & SCAN
   - Exit the skill directory to the parent project root.
   - Run `python skills/latex-template-architect/scripts/scan_codebase.py --source . --ignore vendor`.
   - Read the generated `docs/extracted_meta.json`.

3. AUTO-SYNC MACROS
   - Run `python skills/latex-template-architect/scripts/macro_sync.py --config Preamble/config.tex`.
   - Automatically maps extracted `@tag` values to `\tpl*` macros.

4. MAP INTENT
   - Compare `extracted_items` against `document_structure.chapters`.
   - Generate `mapping_proposals` in `docs/analysis_cache.json`.
```

---

## Workflow 2: Semantic Synthesis (Generate LaTeX)

**Trigger:** "Generate intelligence" / "Synthesize accepted mappings"

```markdown
1. LOAD PROPOSALS
   - Read `docs/analysis_cache.json` -> `mapping_proposals` where status is "accepted".

2. GENERATE SNIPPETS
   - For each proposal, generate a `.tex` snippet in `chapters/generated/`.
   - Format: `\section{...} \begin{quote} ... \end{quote}`.

3. UPDATE CHAPTERS
   - Suggest `\input{chapters/generated/filename.tex}` locations in the terminal.
```

---

## Workflow 3: Studio Verification (Previews & Surgical Builds)

**Trigger:** "Preview layout" / "Isolate [File]"

```markdown
1. SKELETON PREVIEW
   - Run `python skills/latex-template-architect/scripts/latex_studio.py preview --main main.tex`.
   - Compiles a layout-only PDF (no body text) to verify branding and geometry.

2. SURGICAL BUILD
   - Run `python skills/latex-template-architect/scripts/latex_studio.py isolate --target frontmatter/certificate.tex`.
   - Generates a PDF of JUST that component for rapid design checks.
```

---

## Workflow 4: Retrospective & Gap Analysis

**Trigger:** "Retrospect report" / "Perform gap analysis"

```markdown
1. AUDIT COVERAGE
   - List all `extracted_items` that have NO `mapping_proposal`.
   - List all `chapters` that have NO `extracted_items` mapped to them.

2. LOG INCONSISTENCIES
   - Populate `docs/analysis_cache.json` -> `retrospective_report.issues`.

3. SUGGEST IMPROVEMENTS
   - Propose 3-5 structural refinements to the document architecture.
```

---

## Workflow 5: Final Render (Production)

**Trigger:** "Build PDF" / "Render production"

```markdown
1. RENDER DIAGRAMS
   - Run `mmdc -i docs/diagrams/<name>.mmd -o assets/ch_no/<name>.png` for any new diagrams.

2. COMPILE PRODUCTION
   - Use the root `Makefile` -> `make`.
   - Ensure `main/production` mode is active in `config.tex`.

3. APPEND COVERS (Optional)
   - If using external PDF covers:
     - Ensure PDFs are in `external_covers/front/` and `external_covers/back/`
     - Run `make merge EXTERNAL_FRONT=external_covers/front/cover.pdf EXTERNAL_BACK=external_covers/back/cover.pdf`
   - If using LaTeX covers: Skip this step (already included in compilation)

4. VERIFY ARTIFACTS
   - Final check of references, indices, and frontmatter.
```

---

## Workflow 6: External Cover Integration

**Trigger:** "Add custom covers" / "Use external PDFs for front/back"

```markdown
1. PREPARE COVER PDFs
   - Create or download front/back cover PDFs with embedded text boxes
   - Save to: external_covers/front/cover.pdf and external_covers/back/cover.pdf
   - OR modify the defaults provided in external_covers/

2. CONFIGURE MODE (Optional)
   - Edit Preamble/config.tex and set: \newcommand{\tplCoverMode}{external}
   - This is optional—the merge script works regardless of LaTeX settings

3. GENERATE MAIN PDF
   - Run `make all` (generates examples/main.pdf)

4. MERGE WITH COVERS
   - Option A (Explicit):
     make merge EXTERNAL_FRONT=external_covers/front/cover.pdf EXTERNAL_BACK=external_covers/back/cover.pdf
   - Option B (Configured paths):
     make merge

5. OUTPUT
   - Final PDF: examples/main_final.pdf
   - Includes: [Front Cover] + [Main Document] + [Back Cover]
```

---

## Quick Reference: Cover Modes

| Mode | When to Use | Integration |
|:---|:---|:---|
| **LaTeX** (`tplCoverMode=latex`) | Default; use template's cover_front.tex / cover_rear.tex | Automated in `make all` |
| **External** (`tplCoverMode=external`) | Custom PDF covers with special formatting/watermarks | Manual: `make merge` after `make all` |
| **Hybrid** | Use both (LaTeX mode active, but also run merge) | `make all && make merge` |
