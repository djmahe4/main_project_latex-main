# 🚀 Complete Workflow: Clone to Final PDF

This guide walks through the **complete end-to-end process** for using this template in your project repository.

---

## Scenario 1: Standard LaTeX Report (Default)

**Use case:** You want to use the template's built-in LaTeX covers (fastest setup).

### Step 1: Clone the Template
```bash
git clone <your-template-repo> my-report
cd my-report
```

### Step 2: Verify Installation
```bash
make doctor
# Output: ✓ LaTeX installation verified
#         ✓ xelatex found
#         ✓ bibtex found
#         ... etc
```

### Step 3: Configure Project Details
Edit `Preamble/config.tex`:
```latex
\newcommand{\tplProjectTitle}{My Awesome Project}
\newcommand{\tplStudentA}{Your Name}
\newcommand{\tplRegA}{Your Reg ID}
\newcommand{\tplDepartmentName}{Computer Science}
\newcommand{\tplCollegeName}{My College}
\newcommand{\tplProjectGuide}{Professor Name}
% ... edit other macros as needed
```

### Step 4 (Optional): Add Code/Metadata for Scanning
```bash
# If your project has source code to document:
cp -r ~/my-project/src ./project_src/

# Then scan for documentation:
make scan
```

### Step 5: Add Content
- Edit `frontmatter/abstract.tex` — add your abstract
- Edit `frontmatter/acknowledgements.tex` — add acknowledgements
- Add chapter content to `chapters/ch1_introduction.tex`, etc.
- Add figures to `assets/ch1/`, `assets/ch2/`, etc.

### Step 6: Build PDF
```bash
make all
# Output: examples/main.pdf
```

### Step 7: Done!
Open `examples/main.pdf` — your complete report with all covers.

---

## Scenario 2: With External PDF Covers

**Use case:** You have custom designed covers (branding, special formatting, etc.).

### Steps 1-5: Same as Scenario 1

### Step 6a: Prepare External Covers

**Option A: Use Provided Template**
- (Coming soon) `external_covers/template.pptx`
- Edit in PowerPoint → Export to PDF
- Save as `external_covers/front/cover.pdf` and `external_covers/back/cover.pdf`

**Option B: Design Yourself**
- Use PowerPoint, Figma, Canva, Adobe InDesign, etc.
- Dimensions: 8.5" × 11" (US Letter) or A4 (210mm × 297mm)
- Resolution: 300 DPI
- Export to PDF → Place in `external_covers/front/` and `external_covers/back/`

**Option C: Print Provider Template**
- Ask your print provider for their cover template
- Fill in your details (text boxes)
- Export as PDF → Place in `external_covers/`

### Step 6b: Generate Main PDF
```bash
make all
# Output: examples/main.pdf
```

### Step 6c: Merge with Covers
```bash
make merge EXTERNAL_FRONT=external_covers/front/cover.pdf \
           EXTERNAL_BACK=external_covers/back/cover.pdf
# Output: examples/main_final.pdf
```

### Step 7: Done!
Open `examples/main_final.pdf` — complete report with custom covers.

---

## Scenario 3: With Mermaid Diagrams

**Use case:** Your project includes architecture diagrams that should be included in the report.

### Steps 1-5: Same as Scenario 1

### Step 6a: Add Diagrams
Create Mermaid diagram files in `docs/diagrams/`:
```bash
cat > docs/diagrams/architecture.mmd << 'EOF'
graph TD
    A[User] -->|Request| B[API]
    B -->|Query| C[Database]
    C -->|Result| B
    B -->|Response| A
EOF
```

### Step 6b: Render Diagrams to PNG
```bash
# Install mermaid-cli (one time)
npm install -g @mermaid-js/mermaid-cli

# Render all diagrams
mmdc -i docs/diagrams/architecture.mmd -o assets/ch5/architecture.png
```

### Step 6c: Reference in LaTeX
In your chapter files (e.g., `chapters/ch5_system_design.tex`):
```latex
\section{Architecture}
\begin{figure}[h]
    \centering
    \includegraphics[width=0.8\textwidth]{ch5/architecture.png}
    \caption{System Architecture}
    \label{fig:architecture}
\end{figure}
```

### Step 6d: Build PDF
```bash
make all
# Output: examples/main.pdf (with diagrams embedded)
```

---

## Scenario 4: AI-Driven Documentation (Advanced)

**Use case:** Your project has substantial source code and you want the agent to generate documentation chapters automatically.

### Steps 1-5: Same as Scenario 1 + add your code

### Step 6a: Scan Codebase
```bash
make scan
# Output: docs/extracted_meta.json (extracted documentation, comments, diagrams)
```

### Step 6b: Sync Macros
```bash
make sync
# Output: Preamble/config.tex updated with extracted metadata
```

### Step 6c: Preview Layout
```bash
make preview
# Output: docs/preview/skeleton.pdf (layout verification)
```

### Step 6d: Agent Generates Content
The agent will:
1. Read `docs/extracted_meta.json`
2. Propose chapter mappings (code → chapters)
3. Generate LaTeX snippets in `chapters/generated/`
4. Suggest includes to add to `main.tex`

### Step 6e: Finalize & Build
```bash
# Verify generated content, then:
make all
# Output: examples/main.pdf (with AI-generated documentation)
```

---

## Scenario 5: Iterative Development

**Use case:** You're actively developing the report, testing layouts, and want quick previews.

### Quick Build Commands

```bash
# Full rebuild (cleans first)
make clean && make all

# Surgical builds (test individual components)
make isolate TARGET=frontmatter/titlepage.tex
# Output: docs/preview/titlepage.pdf

make isolate TARGET=frontmatter/abstract.tex
# Output: docs/preview/abstract.pdf

# Skeleton preview (no body text, fast)
make preview
# Output: docs/preview/skeleton.pdf

# Health check (verify environment)
make doctor
```

### Debugging Workflow

1. **Catch compilation errors early:**
   ```bash
   make doctor
   make isolate TARGET=chapters/ch1_introduction.tex
   # If OK, try full build:
   make all
   ```

2. **Test specific sections:**
   ```bash
   make isolate TARGET=frontmatter/declaration.tex
   # VS
   make isolate TARGET=chapters/ch3_system_analysis.tex
   ```

3. **Check layout without content:**
   ```bash
   make preview
   ```

---

## Common Tasks

### Add a New Chapter

1. Create file: `chapters/ch10_appendix_code.tex`
   ```latex
   \chapter{Appendix: Code Listings}

   \section{Sample Implementation}
   \input{../assets/code_sample.tex}
   ```

2. Add to `main.tex`:
   ```latex
   \include{chapters/ch10_appendix_code}
   ```

3. Rebuild:
   ```bash
   make all
   ```

### Change Front Cover

**Option A: Modify LaTeX cover**
- Edit `frontmatter/cover_front.tex`
- Rebuild: `make all`

**Option B: Use external PDF**
```bash
cp ~/my-cover.pdf external_covers/front/cover.pdf
make all && make merge
```

### Add Bibliography Entries

1. Edit `references.bib`:
   ```bibtex
   @article{Smith2020,
     title={Example Paper},
     author={Smith, J.},
     journal={Journal},
     year={2020}
   }
   ```

2. Cite in chapters:
   ```latex
   According to \cite{Smith2020}, ...
   ```

3. Rebuild:
   ```bash
   make all
   ```

### Update Project Metadata

Edit `Preamble/config.tex`:
```latex
\newcommand{\tplProjectTitle}{New Title}
\newcommand{\tplSubmissionDate}{April 15, 2025}
```

Then rebuild: `make all`

---

## Installation Troubleshooting

### Issue: `xelatex not found`
```bash
# Linux (Ubuntu/Debian)
sudo apt install texlive-latex-extra texlive-fonts-recommended

# macOS
brew install basictex  # or brew cask install mactex

# Windows
# Download from https://tug.org/texlive/
```

### Issue: `make: command not found`
```bash
# Linux/macOS
# Already installed (comes with build-essential)

# Windows
# Option 1: Use WSL (Windows Subsystem for Linux)
# Option 2: Install git-bash (includes make)
# Option 3: Install GNU Make for Windows
```

### Issue: `pypdf not found` (when merging covers)
```bash
pip install pypdf
# or
pip install -r requirements.txt
```

---

## File Organization for Your Project

```
my-report/
├── main.tex                    # Your report
├── Preamble/
│   ├── config.tex              # ← YOUR EDITS: Project details
│   └── ...
├── frontmatter/
│   ├── abstract.tex            # ← YOUR EDITS: Abstract
│   ├── acknowledgements.tex    # ← YOUR EDITS: Acknowledgements
│   ├── declaration.tex         # ← YOUR EDITS: Declaration
│   └── ...
├── chapters/
│   ├── ch1_introduction.tex    # ← YOUR EDITS: Chapter content
│   ├── ch2_literature_review.tex
│   └── ...
├── assets/
│   ├── ch1/                    # ← YOUR EDITS: Figures for Ch1
│   ├── ch2/
│   └── ...
├── external_covers/            # ← OPTIONAL: Custom PDF covers
│   ├── front/cover.pdf
│   └── back/cover.pdf
├── references.bib              # ← YOUR EDITS: Bibliography
├── examples/
│   └── main.pdf                # ← OUTPUT: Your final report
└── Makefile                    # Build automation
```

---

## Key Files You'll Edit

| File | Purpose | Frequency |
|------|---------|-----------|
| `Preamble/config.tex` | Project metadata (title, authors, etc.) | Once at setup |
| `frontmatter/*.tex` | Front matter (abstract, acknowledgements, etc.) | Multiple times |
| `chapters/*.tex` | Main chapter content | Multiple times |
| `assets/*/` | Images and figures | Multiple times |
| `references.bib` | Bibliography entries | Multiple times |
| `Makefile` | Build configuration | Rarely (already set up) |

---

## What You DON'T Need to Edit

- `Preamble/packages.tex` — LaTeX packages (already configured)
- `Preamble/fonts.tex` — Font setup (already configured)
- `Preamble/pagestyle.tex` — Page style (already configured)
- `main.tex` — Master document includes (already configured)
- `Makefile` — Build automation (ready to use)

---

## Next Steps

1. **Start with Scenario 1** — get your first PDF built
2. **Customize Preamble/config.tex** — add your project details
3. **Add chapter content** — edit `chapters/*.tex` files
4. **Add figures** — place in `assets/` directories
5. **Build & review** — `make all` → open `examples/main.pdf`
6. **Iterate** — refine content, rebuild as needed
7. **(Optional) Add external covers** — follow Scenario 2 if needed

---

## Support & Resources

- **Template documentation**: See `skills/latex-template-architect/skill.md`
- **Workflow details**: See `skills/latex-template-architect/workflows.md`
- **External covers**: See `external_covers/README.md`
- **LaTeX help**: [Overleaf LaTeX Documentation](https://www.overleaf.com/learn)
- **Mermaid diagrams**: [Mermaid Documentation](https://mermaid.js.org/)

---

**Happy reporting! 📄✨**
