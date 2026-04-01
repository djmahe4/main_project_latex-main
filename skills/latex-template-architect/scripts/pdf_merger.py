#!/usr/bin/env python3
"""
PDF Merger for LaTeX Reports
Combines generated main.pdf with optional external front/back covers.

Usage:
    python pdf_merger.py --main examples/main.pdf --output examples/main_final.pdf
    python pdf_merger.py --main examples/main.pdf --front covers/front.pdf --back covers/back.pdf --output examples/main_final.pdf
"""

import argparse
import sys
from pathlib import Path

try:
    from pypdf import PdfWriter, PdfReader
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False
    try:
        from PyPDF2 import PdfMerger, PdfReader, PdfWriter
        PYPDF_AVAILABLE = True
    except ImportError:
        PYPDF_AVAILABLE = False


def validate_pdf(path):
    """Validate that file exists and is readable as PDF."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"PDF not found: {path}")
    if not p.suffix.lower() == '.pdf':
        raise ValueError(f"File is not a PDF: {path}")
    try:
        PdfReader(path)
    except Exception as e:
        raise ValueError(f"Invalid PDF file: {path}\n  Error: {e}")
    return p


def merge_pdfs(main_pdf, front_pdf=None, back_pdf=None, output_path=None):
    """
    Merge PDFs in order: [front] + main + [back]

    Args:
        main_pdf (str|Path): Path to main generated PDF
        front_pdf (str|Path, optional): Path to front cover PDF
        back_pdf (str|Path, optional): Path to back cover PDF
        output_path (str|Path, optional): Output path (defaults to main._final.pdf)

    Returns:
        Path: Output PDF path
    """
    if not PYPDF_AVAILABLE:
        raise ImportError(
            "pypdf not installed. Install with: pip install pypdf"
        )

    # Validate inputs
    main_pdf = validate_pdf(main_pdf)

    front_pdf = validate_pdf(front_pdf) if front_pdf else None
    back_pdf = validate_pdf(back_pdf) if back_pdf else None

    if output_path is None:
        output_path = main_pdf.parent / f"{main_pdf.stem}_final.pdf"
    else:
        output_path = Path(output_path)

    # Create output directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Initialize merger
    try:
        writer = PdfWriter()

        # Add front cover
        if front_pdf:
            front_reader = PdfReader(front_pdf)
            for page_num in range(len(front_reader.pages)):
                writer.add_page(front_reader.pages[page_num])
            print(f"✓ Added front cover: {front_pdf}")

        # Add main document
        main_reader = PdfReader(main_pdf)
        for page_num in range(len(main_reader.pages)):
            writer.add_page(main_reader.pages[page_num])
        print(f"✓ Added main document: {main_pdf} ({len(main_reader.pages)} pages)")

        # Add back cover
        if back_pdf:
            back_reader = PdfReader(back_pdf)
            for page_num in range(len(back_reader.pages)):
                writer.add_page(back_reader.pages[page_num])
            print(f"✓ Added back cover: {back_pdf}")

        # Write output
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

        total_pages = len(writer.pages)
        print(f"\n✓ Merged PDF written: {output_path}")
        print(f"  Total pages: {total_pages}")

        return output_path

    except Exception as e:
        raise RuntimeError(f"Failed to merge PDFs: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Merge LaTeX-generated PDF with optional external covers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Main PDF only (no covers)
  python pdf_merger.py --main examples/main.pdf

  # With external covers
  python pdf_merger.py --main examples/main.pdf \\
    --front external_covers/front/cover.pdf \\
    --back external_covers/back/cover.pdf

  # Custom output path
  python pdf_merger.py --main examples/main.pdf \\
    --output reports/final_report.pdf
        """
    )

    parser.add_argument(
        '--main',
        required=True,
        help='Path to main generated PDF (required)'
    )
    parser.add_argument(
        '--front',
        help='Path to front cover PDF (optional)'
    )
    parser.add_argument(
        '--back',
        help='Path to back cover PDF (optional)'
    )
    parser.add_argument(
        '--output',
        help='Output PDF path (default: main_final.pdf)'
    )

    args = parser.parse_args()

    try:
        output_path = merge_pdfs(
            main_pdf=args.main,
            front_pdf=args.front,
            back_pdf=args.back,
            output_path=args.output
        )
        print(f"\n✅ Success! Output: {output_path}")
        return 0

    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
