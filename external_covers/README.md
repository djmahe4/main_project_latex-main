# External Covers Directory

Store custom front and back covers here for PDF merging with the generated main report.

## Structure

```
external_covers/
├── front/
│   ├── cover.pdf           # Front cover (will be prepended to main.pdf)
│   └── cover_instructions.md
├── back/
│   ├── cover.pdf           # Back cover (will be appended to main.pdf)
│   └── cover_instructions.md
└── README.md               # This file
```

## Usage

### Option 1: Use LaTeX Covers (Default)
This is the default behavior. The template uses:
- `frontmatter/cover_front.tex`
- `frontmatter/cover_rear.tex`

These are automatically included when you run `make all`. No action needed.

### Option 2: Use External PDF Covers

#### Step 1: Create/Prepare Your Covers
Create front and back cover PDFs (8.5" × 11" or A4):
- **Tools**: PowerPoint, Figma, Adobe Design, Canva, or print-to-PDF from any document editor
- **Templates**: Use the provided `cover_template.pptx` (if available) as a starting point
- **Text Boxes**: Leave space for dynamic content, OR pre-fill with your project details

**Size Requirements:**
- Single page (1 PDF page per cover)
- Dimensions: 8.5" × 11" (US Letter) or 210mm × 297mm (A4)
- Resolution: 300 DPI recommended for best quality
- Format: PDF only

#### Step 2: Place Covers in This Directory
```bash
# Copy your files
cp ~/Downloads/my_front_cover.pdf external_covers/front/cover.pdf
cp ~/Downloads/my_back_cover.pdf external_covers/back/cover.pdf
```

#### Step 3: Generate Main PDF
```bash
make all  # Generates examples/main.pdf
```

#### Step 4: Merge with Covers
```bash
# Explicit paths:
make merge EXTERNAL_FRONT=external_covers/front/cover.pdf EXTERNAL_BACK=external_covers/back/cover.pdf

# Or default paths (if placed in this directory with default names):
make merge
```

#### Step 5: Check Output
```
examples/main_final.pdf  ← Your complete report with covers!
```

---

## Examples

### Scenario 1: LaTeX Front, External Back
```bash
# Keep frontmatter/cover_front.tex (LaTeX mode)
# Add external back cover
make merge EXTERNAL_BACK=external_covers/back/cover.pdf
```

### Scenario 2: All External
```bash
# Replace both with external PDFs
make merge \
  EXTERNAL_FRONT=external_covers/front/cover.pdf \
  EXTERNAL_BACK=external_covers/back/cover.pdf
```

### Scenario 3: Batch Processing
```bash
# Regenerate with new covers
make clean
make all
make merge EXTERNAL_FRONT=external_covers/front/new_front.pdf \
           EXTERNAL_BACK=external_covers/back/new_back.pdf
```

---

## Tips for Cover Design

### Recommended Tools

| Tool | Ease | Features |
|:---|:---|:---|
| **PowerPoint** | ⭐⭐⭐⭐⭐ | Drag & drop, export to PDF, templates |
| **Figma** | ⭐⭐⭐⭐ | Free, cloud-based, professional design |
| **Canva** | ⭐⭐⭐⭐⭐ | Templates, easy export |
| **Adobe InDesign** | ⭐⭐⭐ | Professional, steep learning curve |
| **LibreOffice Draw** | ⭐⭐⭐ | Free, desktop-based |

### Design Checklist

- [ ] Dimensions: 8.5" × 11" or A4 (210mm × 297mm)
- [ ] Resolution: 300 DPI
- [ ] All text is embedded (not linked)
- [ ] No transparency (unless intentional)
- [ ] Color mode: RGB or CMYK (avoid grayscale if color printing)
- [ ] Margins: 0.25" minimum from edges
- [ ] Tested: Export to PDF and verify appearance
- [ ] Text is visible (sufficient contrast with background)

### Customization Ideas

**Front Cover typically includes:**
- Project title
- Student/Team names
- Institution logo
- Department/Course
- Date
- Project year

**Back Cover typically includes:**
- Acknowledgements or executive summary
- Project team photo (optional)
- Institution contact info
- QR code to digital version (optional)

---

## Troubleshooting

### PDF Merge Fails
**Error:** `PDF not found` or `Invalid PDF`

**Solution:**
1. Check file exists: `ls external_covers/front/cover.pdf`
2. Verify it's a valid PDF: Open in Adobe Reader or Preview
3. Ensure file permissions: `chmod 644 external_covers/front/cover.pdf`

### Wrong Page Order
**Issue:** Cover appears in middle or wrong position

**Solution:**
- Check Makefile: Front should use `--front`, Back should use `--back`
- Verify merge command: `make merge EXTERNAL_FRONT=... EXTERNAL_BACK=...`

### Text Not Showing
**Issue:** Cover PDF appears blank in final output

**Solution:**
1. Test cover PDF standalone (open in PDF viewer)
2. Check if PDF uses embedded fonts or linked fonts
3. Try re-exporting from source tool

### Page Size Mismatch
**Issue:** Cover appears larger/smaller than main document

**Solution:**
- Regenerate covers in exact same size as main.pdf
- Check main.pdf page size: `pdfinfo examples/main.pdf | grep "Page size"`
- Then regenerate covers with that exact size

---

## Advanced: Python API

```python
from skills.latex_template_architect.scripts.pdf_merger import merge_pdfs

# Merge programmatically
output = merge_pdfs(
    main_pdf='examples/main.pdf',
    front_pdf='external_covers/front/cover.pdf',
    back_pdf='external_covers/back/cover.pdf',
    output_path='examples/my_report_final.pdf'
)

print(f"Created: {output}")
```

---

## FAQ

**Q: Can I use covers from different sources (e.g., student-designed front, template back)?**
A: Yes! Simply provide separate paths: `make merge EXTERNAL_FRONT=... EXTERNAL_BACK=...`

**Q: What if I only want a front cover (no back)?**
A: Use only `EXTERNAL_FRONT`: `make merge EXTERNAL_FRONT=external_covers/front/cover.pdf`

**Q: Will external covers affect page numbering?**
A: No. The main document's page numbering (Chapter 1, page 1) remains unchanged. Covers are outside the numbering scheme.

**Q: Can I embed text dynamically in covers?**
A: Not automatically, but you can:
1. Use LaTeX mode (see `frontmatter/cover_front.tex`)
2. Pre-fill your PDF with all text before placing here
3. Add text interactively (e.g., using PDFs with form fields, then fill programmatically)

**Q: What if my printer requires specific formats?**
A: Check with your print vendor's PDF requirements, then prepare covers accordingly. Common requirements:
- CMYK color space (add by re-exporting from design tool with CMYK output)
- 300 DPI minimum resolution
- Bleed marks (typically 0.125" beyond trim line)

---

## See Also

- `skills/latex-template-architect/scripts/pdf_merger.py` — Python merge implementation
- `Preamble/config.tex` — Cover mode configuration
- `frontmatter/cover_*.tex` — LaTeX cover alternatives
