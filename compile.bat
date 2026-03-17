@echo off
echo Compiling LaTeX document...
if not exist logs mkdir logs
if not exist logs\frontmatter mkdir logs\frontmatter
if not exist logs\chapters mkdir logs\chapters

echo Pass 1: xelatex...
xelatex -output-directory=logs -interaction=nonstopmode main.tex

echo Pass 2: bibtex...
bibtex logs/main

echo Pass 3: xelatex...
xelatex -output-directory=logs -interaction=nonstopmode main.tex

echo Pass 4: xelatex...
xelatex -output-directory=logs -interaction=nonstopmode main.tex

move /Y logs\main.pdf .
echo Done!
