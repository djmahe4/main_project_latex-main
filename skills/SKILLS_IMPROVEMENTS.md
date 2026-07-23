# Skills Folder Audit & Multi-Project Generalization Plan

## 1. Executive Summary
This document summarizes the architectural differences between the baseline template repository (`main_project_latex-main`) and the project-specific instance (`footydj_mini_project/main_project_latex-main`), records the hardcoded domain elements identified within the `skills/` folder, and outlines the structural refactoring performed to make the template reusable across multiple engineering software projects.

---

## 2. Baseline Template vs. Project Instance Comparison

| Component | Baseline Template (`main_project_latex-main`) | Active Instance (`footydj_mini_project`) |
| :--- | :--- | :--- |
| **Directory Scope** | Universal template structure | Project-specific output & build logs |
| **Automation Scripts** | Core workflow scripts (`scan_codebase.py`, `narrative_expander.py`, etc.) | Custom inline scripts (`apply_tikz.py`, `update_appendices.py`, `debug_sync.py`) |
| **Build State** | Clean (No compiled `.pdf`, `.aux`, `.log` artifacts) | Populated with compiled `main.pdf` & intermediate output files |
| **Skills Infrastructure** | Includes `code-documentation-architect`, `latex-template-architect`, `docs` | Same, with pre-populated project metadata |

---

## 3. Audit of Hardcoded Content in `skills/`

Prior to refactoring, the template contained project-specific bindings to **FootyDJ** (Football Video & Music Synchronization system):

1. **Script References (`skills/latex-template-architect/scripts/`)**:
   - `apply_tikz_meta.py`: Hardcoded absolute Windows paths (`c:\Users\mahes\...\footydj_mini_project\...`) pointing directly to active project files.
   - `diagram_converter.py`: Bound to absolute FootyDJ `extracted_meta.json` file paths.
   - `narrative_expander.py`: Hardcoded prompts requesting synthesis for "FootyDJ project metadata" and enforcing domain terms (e.g., YOLO, ByteTrack, OSNet, COCOMO).

2. **Skill Documentation (`skills/code-documentation-architect/`)**:
   - `customization.md`: Chapter 6 auto-generated section listings and performance metric tables pre-configured with FootyDJ specific modules (e.g., *Video Trimmer Module*, *Pitch Registration Engine*, *YOLOv8 Inference Latency*).

3. **Metadata Stores (`skills/docs/`)**:
   - `extracted_meta.json` & `logical_summaries.json`: Embedded domain metadata for soccer highlight processing.

---

## 4. Performed Refactoring & Multi-Project Enhancements

To transform the template into a modular, multi-project solution, the following changes were applied:

1. **Dynamic Pathing & Environment Override**:
   - Replaced absolute paths in `apply_tikz_meta.py` and `diagram_converter.py` with dynamic `os.getenv("PROJECT_META_PATH", os.path.join("skills", "docs", "extracted_meta.json"))`.

2. **Parametrized LLM Narrative Expander**:
   - Updated `narrative_expander.py` to ingest `PROJECT_NAME`, `PROJECT_META_PATH`, and LLM endpoint parameters from environment variables, eliminating rigid FootyDJ references.

3. **Project Configuration Schema**:
   - Created [`project_config.template.json`](file:///C:/Users/mahes/OneDrive/Desktop/Python-Projects/main_project_latex-main/project_config.template.json) to allow new projects to declare domain keywords, metadata locations, and custom prompts without editing core skill scripts.

5. **Preamble Config & Chapter Schema Enhancements**:
   - Extended [`Preamble/config.tex`](file:///C:/Users/mahes/OneDrive/Desktop/Python-Projects/main_project_latex-main/Preamble/config.tex) with an extensible **Technology & Component Placeholders** block (`\tplSystemArchitecture`, `\tplAPILayer`, `\tplDatabaseEngine`, `\tplAIService`, `\tplModelEngine`) preventing LaTeX compilation errors across projects.
   - Updated [`chapters/ch1_introduction.tex`](file:///C:/Users/mahes/OneDrive/Desktop/Python-Projects/main_project_latex-main/chapters/ch1_introduction.tex) with commented snippet templates for TikZ diagrams, component citations, and figure formatting.

---

## 5. Standardized Multi-Project Workflow

For any new software project utilizing this LaTeX template:

1. **Copy Baseline Template**:
   ```bash
   cp -r main_project_latex-main my_new_project_report
   ```
2. **Configure Domain Metadata**:
   Copy `project_config.template.json` to `project_config.json` and set `project_name` and domain parameters.
3. **Execute Pipeline**:
   ```bash
   export PROJECT_NAME="MyNewProject"
   python skills/latex-template-architect/scripts/scan_codebase.py
   python skills/latex-template-architect/scripts/narrative_expander.py
   make pdf
   ```
