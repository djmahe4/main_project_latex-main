# 📄 LaTeX Final Year Project Report Template

A **reusable, modular LaTeX template** for engineering final-year project reports.
Built for XeLaTeX with a clean chapter-based structure, automated PDF compilation, and diagram integration.

---

## 📁 Folder Structure

```
main_project_latex-main/
├── main.tex                  # Master document — includes all parts
├── references.bib            # BibTeX bibliography database
├── compile.sh                # Build script (Linux / macOS)
├── compile.bat               # Build script (Windows)
│
├── Preamble/                 # Modular LaTeX preamble
│   ├── packages.tex          # All \usepackage declarations
│   ├── fonts.tex             # Font configuration (XeLaTeX)
│   ├── pagestyle.tex         # Page geometry, headers, footers
│   ├── sectionoptions.tex    # Chapter/section/ToC formatting
│   └── macro.tex             # Project macros, hyperref, listings
│
├── frontmatter/              # Pages before Chapter 1
│   ├── cover_front.tex       # Soft-binding front cover (PDF page 1)
│   ├── cover_rear.tex        # Soft-binding rear cover (last PDF page)
│   ├── titlepage.tex         # Inner title page
│   ├── certificate.tex       # Supervisor certificate
│   ├── declaration.tex       # Student declaration
│   ├── acknowledgements.tex  # Acknowledgements
│   ├── abstract.tex          # Abstract
│   └── abbreviations.tex     # List of abbreviations
│
├── chapters/                 # Main content (CH1–CH9 + back matter)
│   ├── ch1_introduction.tex
│   ├── ch2_literature_review.tex
│   ├── ch3_system_analysis.tex
│   ├── ch4_methodology.tex
│   ├── ch5_system_design.tex
│   ├── ch6_system_implementation.tex
│   ├── ch7_testing.tex
│   ├── ch8_results.tex
│   ├── ch9_conclusions.tex
│   ├── list_of_publications.tex
│   └── appendices.tex
│
├── assets/                   # Images, logos, and figures
│   ├── PRCLogo.png
│   ├── header.png
│   ├── ch1/ … ch5/           # Per-chapter figure assets
│   └── …
│
├── docs/                     # Documentation and diagrams
│   └── diagrams/
│       ├── structure.mmd     # Mermaid: repo structure mindmap
│       ├── build-flow.mmd    # Mermaid: build + artifact flowchart
│       ├── structure.png     # Generated PNG (via mmdc)
│       └── build-flow.png    # Generated PNG (via mmdc)
│
├── examples/                 # ✅ Compiled output — mirrors repo structure
│   ├── main.pdf              # Generated PDF (mirrors main.tex)
│   ├── docs/
│   │   └── diagrams/
│   │       ├── structure.png # Generated PNG (mirrors docs/diagrams/structure.mmd)
│   │       └── build-flow.png# Generated PNG (mirrors docs/diagrams/build-flow.mmd)
│   └── README.md             # Output directory documentation
│
└── skills/                   # Automation skill definitions
    └── latex-template/
        ├── skill.md          # Core skill behaviour
        ├── rules.md          # Structural and formatting rules
        └── workflows.md      # Step-by-step automation workflows
```

---

## 🚀 Quick Start

### Prerequisites

| Tool | Purpose |
|------|---------|
| [TeX Live](https://tug.org/texlive/) or [MiKTeX](https://miktex.org/) | LaTeX distribution |
| `xelatex` | Compiler (required for font support) |
| `bibtex` | Bibliography processor |
| [Node.js](https://nodejs.org/) + `mmdc` | Mermaid diagram generation (optional) |

### Compile the PDF

**Linux / macOS:**
```bash
chmod +x compile.sh
./compile.sh
# Output → examples/main.pdf
```

**Windows:**
```bat
.\compile.bat
REM Output → examples\main.pdf
```

**Manual (step-by-step):**
```bash
mkdir -p logs examples
xelatex -output-directory=logs -interaction=nonstopmode main.tex
bibtex logs/main
xelatex -output-directory=logs -interaction=nonstopmode main.tex
xelatex -output-directory=logs -interaction=nonstopmode main.tex
mv logs/main.pdf examples/
```

---

## ✏️ Customisation Guide

### 1. Project details (`Preamble/macro.tex`)
Change the title, authors, department, and college:
```latex
\newcommand{\thetitle}{Your Project Title}
\newcommand{\studentA}{FULL NAME}
\newcommand{\regA}{ROLLNUMBER}
\newcommand{\thedepartment}{Your Department}
\newcommand{\thecollege}{Your College}
```

### 2. Front matter (`frontmatter/`)
Edit individual files:
- `cover_front.tex` — soft-binding front cover
- `titlepage.tex` — inner title page
- `acknowledgements.tex` — acknowledgements text
- `abstract.tex` — project abstract
- `abbreviations.tex` — list of abbreviations

### 3. Chapters (`chapters/`)
Each chapter is a standalone `.tex` file included via `\include{}` in `main.tex`.
Add content directly or create new chapter files and add the include:
```latex
\include{chapters/ch10_future_work}
```

### 4. Figures (`assets/`)
Place figures in the relevant sub-folder (e.g., `assets/ch3/`).
Reference them as:
```latex
\includegraphics[width=0.8\textwidth]{ch3/my_figure.png}
```

### 5. Bibliography (`references.bib`)
Add BibTeX entries and cite with `\cite{key}`.

---

## 📊 Diagrams (Mermaid + mmdc)

Diagram sources live in `docs/diagrams/` as `.mmd` files.
Generate PNGs with [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli):

```bash
npm install -g @mermaid-js/mermaid-cli

mmdc -i docs/diagrams/structure.mmd   -o examples/docs/diagrams/structure.png
mmdc -i docs/diagrams/build-flow.mmd  -o examples/docs/diagrams/build-flow.png
```

---

## 📦 Output (`examples/`)

All compiled artifacts are stored in `examples/`, **mirroring the source structure**:

| Artifact | Source | Output in `examples/` |
|----------|--------|----------------------|
| PDF report | `main.tex` | `examples/main.pdf` |
| Structure diagram | `docs/diagrams/structure.mmd` | `examples/docs/diagrams/structure.png` |
| Build-flow diagram | `docs/diagrams/build-flow.mmd` | `examples/docs/diagrams/build-flow.png` |

Intermediate build files (`.aux`, `.log`, `.toc`, etc.) are written to `logs/`
and are ignored by `.gitignore`.

---

## 📋 Document Structure (Table of Contents order)

| Section | Numbering |
|---------|-----------|
| Soft-binding Front Cover | — |
| Title Page, Certificate, Declaration | — |
| Acknowledgements | roman (i) |
| Abstract | roman |
| List of Figures | roman |
| List of Tables | roman |
| List of Abbreviations | roman |
| **CHAPTER 1: INTRODUCTION** | arabic (1) |
| CHAPTER 2: LITERATURE REVIEW | |
| CHAPTER 3: SYSTEM ANALYSIS | |
| CHAPTER 4: METHODOLOGY | |
| CHAPTER 5: SYSTEM DESIGN | |
| CHAPTER 6: SYSTEM IMPLEMENTATION | |
| CHAPTER 7: TESTING | |
| CHAPTER 8: RESULTS | |
| CHAPTER 9: CONCLUSIONS | |
| References | |
| List of Publications | |
| Appendix 1: Sample Code | |
| Appendix 2: Bills of Purchased Materials | |
| Soft-binding Rear Cover | — |

---

## 📄 License

This template is provided for academic use.
