# 📋 Layout & Design Preview Report

This document tracks the current "Visual Schema" of the LaTeX project. Use the commands below to generate and verify design artifacts.

## 🎨 Active Design Variants
| Variant | Status | Last Build | Preview Link |
| :--- | :--- | :--- | :--- |
| **Example Template** | `In Progress(Out-of-sync with the template)` | - | [example_firmai.pdf](../examples/example_firmai.pdf) |
| **Actual Template**| `Should be in sync with the template` | - | [main.pdf](../examples/main.pdf) |
| **Final PDF with External Covers** | `In Progress` | - | [main_final.pdf](../examples/main_final.pdf) |

## 🧪 Surgical Builds (Isolated Previews)
Run these commands to build specific pages/components in isolation:

| Artifact | Command | Description |
| :--- | :--- | :--- |
| **Title Page** | `make titlepage` | Verify logos, fonts, and placement on the cover. |
| **Abstract** | `make isolate TARGET=frontmatter/abstract` | Verify paragraph styling and headers. |
| **Fonts** | `make isolate TARGET=Preamble/fonts` | Run a font pangram test (requires `fonts_test.tex`). |

## 📐 Template Settings (Baseline)
- **Primary Font**: `\tplRomanFont`
- **Mono Color**: `\tplMonoFontColor`
- **Branding**: Logos located in `assets/`

> [!TIP]
> Use `make clean` before a full build if you've been doing many isolated previews to avoid `.aux` file pollution.
