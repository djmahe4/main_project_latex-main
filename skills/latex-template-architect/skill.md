---
name: latex-template-architect
mode: reusable
version: "3.5"
---

# LaTeX Intelligent Documentation Architect (v3.5)

> [!IMPORTANT]
> All documentation generation is governed by the [Engineering Rules & Structural Standards](./rules.md). AI Agents MUST comply with the immutable directory structure and formatting constraints defined therein.

## Phases

The `latex-template-architect` skill operates in three phases:

1. **Analysis**: Extract metadata from the codebase, identifying key elements such as headings, lists, tables, and code snippets.
2. **Transformation**: Convert the extracted metadata into LaTeX-compatible format, applying structural integrity and semantic transformation rules.
3. **Synthesis**: Ingest the transformed metadata and update the corresponding `.tex` chapters, ensuring a cohesive and well-structured document.

## Requirements

To ensure the production of high-quality LaTeX documents, the skill must adhere to the following standards:

* **Structural Integrity**: Preserve the hierarchical structure of the metadata, using appropriate LaTeX environments such as `section`, `subsection`, and `subsubsection`.
* **Semantic Transformation**: Accurately convert Markdown-like metadata into professional LaTeX environments, including:
  - Lists (ordered and unordered) to `enumerate` and `itemize` environments.
  - Tables to `tabular` environments.
  - Code snippets to `lstlisting` or `verbatim` environments.
* **Consistency**: Maintain consistency in formatting, spacing, and styling throughout the document.

## Guidelines

* Use LaTeX environments and commands to create structured documents.
* Apply semantic transformation rules for all auto-generated content.
* Ensure clear and concise headings, subheadings, and captions.

---

## 2. Analysis Cache & Retrospect

### Intelligence Schema (`docs/analysis_cache.json`):
- `extracted_items`: Raw snippets with lineage.
- `mapping_proposals`: Suggested `item_id -> chapter_id` links.
- `retrospective_report`: Log of logical inconsistencies (e.g., "Code in `src/legacy` is undocumented").

### The Retrospect Workflow:
After initial synthesis, perform a "Gap Analysis":
1. Compare `extracted_items` vs. `mapping_proposals` to find missed sub-systems.
2. Verify that all Mermaid diagrams are correctly referenced in the text.
3. Suggest structural refinements based on discovered code complexity.

---

## 3. Automation Commands

| Command | Action | Description |
| :--- | :--- | :--- |
| `make scan` | `scan_codebase.py` | Extracts project metadata into `docs/extracted_meta.json`. |
| `make sync` | `macro_sync.py` | Maps metadata `@tags` to LaTeX preamble macros. |
| `make preview` | `latex_studio.py` | Generates a layout-only Skeleton PDF. |
| `make isolate` | `latex_studio.py` | Builds a single `.tex` file in isolation for design checks. |
| `make doctor` | `architect_doctor.py` | Performs a system health check. |
| `make merge` | `pdf_merger.py` | Merges external PDF covers with generated main.pdf (optional). |

> [!TIP]
> Each automation tool supports a comprehensive CLI interface via `argparse`. For a full list of arguments, defaults, and advanced usage, refer to the [Scripts Reference Guide](./scripts.md).

---

## 4. Intelligent Initiation (Workflow Snapshot)
1.  **Doctor**: Run `python skills/latex-template-architect/scripts/architect_doctor.py` to verify the environment.
2.  **Scan**: Run `python skills/latex-template-architect/scripts/scan_codebase.py --source .` to populate metadata.
3.  **Sync**: Run `python skills/latex-template-architect/scripts/macro_sync.py` to auto-populate the LaTeX preamble.

---

## 4. Environment Safety & Pathing

- **Root Detection**: Project root is defined by the presence of `main.tex` and `Preamble/`.
- **Governance**: Refer to [rules.md](./rules.md) for immutable path constraints and mandatory compilation sequences.
- **Targeting**: When running from sub-folders, always prepend paths with root-relative logic.
