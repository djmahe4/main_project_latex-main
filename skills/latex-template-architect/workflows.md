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

3. VERIFY ARTIFACTS
   - Final check of references, indices, and frontmatter.
```
