# LaTeX Architect - Scripts Reference (v3.5)

This document provides a detailed reference for the automation scripts contained in `skills/latex-template-architect/scripts/`.

> [!NOTE]
> All script defaults are aligned with the standards defined in [rules.md](./rules.md). Overriding these defaults via CLI arguments should be done with caution to maintain project structural integrity.

## 1. scan_codebase.py
**Purpose:** Recursively scans the project directory for documentation metadata (docstrings, comments, Mermaid diagrams).

| Argument | Default | Description |
| :--- | :--- | :--- |
| `--source` | `.` | Directory to scan for source files. |
| `--output` | `docs/extracted_meta.json` | Path to save the extracted JSON results. |
| `--ignore` | `[.git, node_modules, ...]` | List of directory names to exclude from the scan. |

**Example:**
```bash
python scripts/scan_codebase.py --source ./src --ignore vendor tests
```

---

## 2. macro_sync.py
**Purpose:** Maps extracted metadata `@tags` to LaTeX `\tpl*` macros in the configuration preamble.

| Argument | Default | Description |
| :--- | :--- | :--- |
| `--config` | `Preamble/config.tex` | Path to the LaTeX configuration file. |
| `--meta` | `docs/extracted_meta.json` | Path to the source extraction metadata. |

**Example:**
```bash
python scripts/macro_sync.py --config Preamble/custom_config.tex
```

---

## 3. latex_studio.py
**Purpose:** Manages specialized build modes (Skeleton Previews and Isolated Component Rendering).

| Argument | Default | Description |
| :--- | :--- | :--- |
| `mode` | *(Required)* | Either `preview` (Layout only) or `isolate` (Single file). |
| `--target` | `None` | The .tex file to build in `isolate` mode. |
| `--main` | `main.tex` | The root file used for skeleton injection. |
| `--output` | `docs/preview` | Directory for the generated PDF outputs. |
| `--engine` | `xelatex\|pdflatex` | Override the default LaTeX engine. |

**Example:**
```bash
python scripts/latex_studio.py isolate --target chapters/introduction.tex
```

---

## 4. architect_doctor.py
**Purpose:** Performs a system health check to ensure all assets and tools are ready.

| Argument | Default | Description |
| :--- | :--- | :--- |
| `--root` | `.` | Project root directory to check. |
| `--skip-latex` | `False` | Skip verification of LaTeX engines (xelatex/pdflatex). |

**Example:**
```bash
python scripts/architect_doctor.py --skip-latex
```
