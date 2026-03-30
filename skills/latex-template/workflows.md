# Automation Workflows

## Workflow 1: Generate a New Report

**Trigger:** "Generate a new LaTeX report for [title] by [authors] in [domain]"

```
1. SCAN
   - Read Preamble/macro.tex  → extract all \newcommand project macros
   - Read main.tex            → note include order and page numbering
   - Read examples/main.pdf   → confirm visual style

2. UPDATE MACROS (Preamble/macro.tex)
   - Set \thetitle, \studentA–D, \regA–D
   - Set \thedepartment, \thecollege, \theyear
   - Set \theprojectguide, \thehod, etc.

3. UPDATE FRONTMATTER
   - frontmatter/abstract.tex   → write project-specific abstract
   - frontmatter/abbreviations.tex → populate abbreviations table

4. GENERATE CHAPTER STUBS
   For each required chapter:
   - chapters/ch1_introduction.tex   → \chapter{INTRODUCTION} + section stubs
   - chapters/ch2_literature_review.tex → …
   - … through ch9_conclusions.tex

5. COMPILE
   ./compile.sh
   → Verify examples/main.pdf was created

6. GENERATE DIAGRAMS
   mmdc -i docs/diagrams/structure.mmd  -o examples/docs/diagrams/structure.png
   mmdc -i docs/diagrams/build-flow.mmd -o examples/docs/diagrams/build-flow.png
```

---

## Workflow 2: Add a New Chapter

**Trigger:** "Add chapter [N]: [TITLE]"

```
1. Create chapters/chN_<slug>.tex with:
   \chapter{UPPERCASE TITLE}
   \section{Introduction}
   % placeholder content

2. Insert in main.tex after the preceding chapter include:
   \include{chapters/chN_<slug>}

3. Compile to verify ToC entry appears:
   ./compile.sh
```

---

## Workflow 3: Generate / Regenerate Diagrams

**Trigger:** "Generate diagrams" / "Update diagrams"

```
1. Write / update .mmd files in docs/diagrams/

2. Run mmdc for each file:
   mmdc -i docs/diagrams/structure.mmd   -o examples/docs/diagrams/structure.png
   mmdc -i docs/diagrams/build-flow.mmd  -o examples/docs/diagrams/build-flow.png
   # Add further diagrams as needed (e.g., inclusion.mmd, workflow.mmd, pipeline.mmd)

3. Confirm PNG files exist in examples/docs/diagrams/
```

---

## Workflow 4: Full Rebuild from Scratch

**Trigger:** "Clean build" / "Rebuild PDF"

```
1. Remove old artifacts:
   rm -rf logs/
   rm -f examples/main.pdf

2. Compile fresh:
   ./compile.sh

3. Verify:
   ls -lh examples/main.pdf
```

---

## Workflow 5: Deep Scan Report

**Trigger:** "Scan this repo" / "Analyse template"

```
Output a structured report containing:

## Project Details
- Title, authors, department, college (from Preamble/macro.tex)

## Document Structure
- List of all \include{} calls in main.tex, in order
- Page numbering zones (gobble / roman / arabic)

## Packages Used
- All \usepackage{} calls from Preamble/packages.tex

## Formatting Summary
- Fonts, geometry, spacing (from pagestyle.tex, fonts.tex)
- Chapter/section format (from sectionoptions.tex)

## Figures Inventory
- All files in assets/ with their chapter associations

## Build Configuration
- Compiler, passes, output location (from compile.sh)
```

---

## Workflow 6: Validate Structure

**Trigger:** "Validate template" / "Check structure"

```
Checks (report PASS / FAIL for each):

□ main.tex exists
□ All \include{} targets exist as .tex files
□ Preamble/ has: packages.tex fonts.tex pagestyle.tex sectionoptions.tex macro.tex
□ frontmatter/ has: cover_front.tex cover_rear.tex titlepage.tex abstract.tex
□ chapters/ has: ch1 through ch9, list_of_publications, appendices
□ assets/ contains at least one image file
□ references.bib exists
□ compile.sh is executable
□ examples/ directory exists
□ docs/diagrams/ contains .mmd files
```
