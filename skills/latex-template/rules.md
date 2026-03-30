# Structural and Formatting Rules

## 🔒 Immutable Structure

Never rename, delete, or flatten these paths:

```
main.tex
references.bib
compile.sh
compile.bat
Preamble/
frontmatter/
chapters/
assets/
README.md
.gitignore
```

---

## 📁 Directory Conventions

| Directory | Purpose | Mutable? |
|-----------|---------|----------|
| `Preamble/` | LaTeX preamble files | Contents editable; do not remove files |
| `frontmatter/` | Pre-chapter pages | Contents editable |
| `chapters/` | Main document chapters | Add/edit; never remove existing |
| `assets/` | Images and figures | Add freely |
| `examples/` | Compiled output | Auto-generated; `main.pdf` tracked |
| `docs/diagrams/` | Mermaid sources | Add `.mmd` files; PNGs are generated |
| `skills/` | Skill system files | Editable |
| `logs/` | Build intermediates | Auto-generated; fully gitignored |

---

## 📑 Document Ordering Rules

### Front Matter (roman numerals)
1. Soft-binding front cover — `\pagenumbering{gobble}`
2. Title page
3. Certificate
4. Declaration
5. Acknowledgements — `\chapter*` + `\addcontentsline`
6. Abstract — `\chapter*` + `\addcontentsline`
7. Table of Contents
8. List of Figures — `\addcontentsline`
9. List of Tables — `\addcontentsline`
10. List of Abbreviations — `\chapter*` + `\addcontentsline`

### Main Matter (arabic numerals, reset to 1)
- CH1 through CH9 in sequential order
- Each chapter uses `\chapter{UPPERCASE TITLE}`

### Back Matter
1. References — `\addcontentsline{toc}{chapter}{REFERENCES}` before `\bibliography{}`
2. List of Publications — `\chapter*` + `\addcontentsline`
3. Appendix 1: Sample Code — `\chapter*` + `\addcontentsline`
4. Appendix 2: Bills of Purchased Materials — `\chapter*` + `\addcontentsline`
5. Soft-binding rear cover — `\pagenumbering{gobble}`

---

## 🎨 Formatting Rules

### Fonts (XeLaTeX)
- Roman: Times New Roman
- Sans: Arial
- Mono: Courier New

### Page geometry
- Margins: 1 in on all sides
- `headheight`: 40pt (for header image)
- Header: right-aligned logo image (`header.png`)
- Footer: centred page number

### Chapter headings
- Numbered: `\titleformat{\chapter}[display]{\centering\bfseries\Huge}{\chaptertitlename\ \thechapter}{...}`
- Unnumbered: same style without number

### ToC entries
- Chapter entries have dot leaders: `\renewcommand{\cftchapleader}{\cftdotfill{\cftdotsep}}`
- `\cftbeforechapskip = 6pt` — prevents run-together entries
- `\cftbeforesecskip = 2pt`
- `\cftbeforesubsecskip = 1pt`

### Spacing
- `\onehalfspacing`
- `\parindent = 0pt`
- `\parskip = 6pt`

---

## ⚙️ Compilation Rules

- Compiler: **xelatex** (required for font support)
- Build sequence: `xelatex → bibtex → xelatex → xelatex`
- Intermediate artifacts → `logs/`
- Final PDF → `examples/main.pdf`
- Never commit `logs/` contents

