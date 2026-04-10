#!/usr/bin/env python3
"""
Validate Code-to-Documentation Mappings

Cross-checks extracted code artifacts against LaTeX chapter references.
Identifies orphaned artifacts (code with no docs) and broken references (docs with no code).

Usage:
    python validate_mappings.py --metadata docs/code_metadata.json --latex-dir Chapters/
    python validate_mappings.py --check-orphaned REQ --check-broken-refs
"""

import json
import re
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of mapping validation"""
    artifact_id: str
    status: str  # 'OK', 'ORPHANED', 'BROKEN_REF'
    message: str
    chapter: str
    file: str


class MappingValidator:
    """Validates bidirectional mappings between code and LaTeX"""
    
    def __init__(self):
        self.artifacts: Dict[str, Dict] = {}
        self.latex_references: Set[str] = set()
        self.results: List[ValidationResult] = []
    
    def load_metadata(self, metadata_file: Path) -> None:
        """Load extracted code metadata"""
        with open(metadata_file) as f:
            data = json.load(f)
            for artifact in data.get('artifacts', []):
                self.artifacts[artifact['artifact_id']] = artifact
        
        print(f"Loaded {len(self.artifacts)} artifacts from metadata")
    
    def scan_latex_references(self, latex_dir: Path) -> None:
        """Scan LaTeX files for artifact references"""
        pattern = r'\\ref\{([^}]*:([A-Z]+[A-Z0-9\-]*)\)\}'
        
        for tex_file in latex_dir.glob('*.tex'):
            try:
                with open(tex_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Find all \ref{} commands
                    for match in re.finditer(pattern, content):
                        ref = match.group(2)  # Extract artifact ID
                        self.latex_references.add(ref)
                    
                    # Also find direct artifact ID mentions in comments
                    for match in re.finditer(r'(?:CODE|REQ|ARCH|SEQ|API|TC|PERF)-\d{3}', content):
                        self.latex_references.add(match.group(0))
            
            except UnicodeDecodeError:
                print(f"Warning: Could not read {tex_file}")
        
        print(f"Found {len(self.latex_references)} artifact references in LaTeX")
    
    def validate_mappings(self, check_orphaned: bool = True, 
                         check_broken: bool = True) -> List[ValidationResult]:
        """Validate bidirectional mappings"""
        self.results = []
        
        # Check for orphaned code artifacts (code with no LaTeX reference)
        if check_orphaned:
            for artifact_id, artifact in self.artifacts.items():
                if artifact_id not in self.latex_references:
                    self.results.append(ValidationResult(
                        artifact_id=artifact_id,
                        status='ORPHANED',
                        message=f"Code artifact not referenced in LaTeX documentation",
                        chapter=artifact['chapter'],
                        file=artifact['file_path']
                    ))
        
        # Check for broken references (LaTeX references with no code artifact)
        if check_broken:
            for ref in self.latex_references:
                if ref not in self.artifacts:
                    self.results.append(ValidationResult(
                        artifact_id=ref,
                        status='BROKEN_REF',
                        message=f"LaTeX reference not found in code metadata",
                        chapter='UNKNOWN',
                        file='UNKNOWN'
                    ))
        
        # Mark valid mappings
        for artifact_id in self.artifacts:
            if artifact_id in self.latex_references:
                self.results.append(ValidationResult(
                    artifact_id=artifact_id,
                    status='OK',
                    message='Artifact properly mapped',
                    chapter=self.artifacts[artifact_id]['chapter'],
                    file=self.artifacts[artifact_id]['file_path']
                ))
        
        return self.results
    
    def get_statistics(self) -> Dict[str, int]:
        """Get validation statistics"""
        stats = {
            'total': len(self.results),
            'valid': len([r for r in self.results if r.status == 'OK']),
            'orphaned': len([r for r in self.results if r.status == 'ORPHANED']),
            'broken_refs': len([r for r in self.results if r.status == 'BROKEN_REF']),
        }
        return stats
    
    def trace_to_requirements(self, prefix: str) -> Dict[str, List[str]]:
        """Trace design/implementation artifacts back to requirements"""
        traceability = {}
        
        # Parse artifact prefix (e.g., 'ARCH', 'CODE')
        for artifact_id, artifact in self.artifacts.items():
            if artifact_id.startswith(prefix):
                related_reqs = []
                
                # Look for related REQ-* in tags or description
                description = artifact.get('description', '')
                doc_tags = artifact.get('doc_tags', {})
                
                related_ids = doc_tags.get('related_artifacts', [])
                if isinstance(related_ids, str):
                    related_ids = [related_ids]
                
                for related in related_ids:
                    if related.startswith('REQ-'):
                        related_reqs.append(related)
                
                if related_reqs:
                    traceability[artifact_id] = related_reqs
                else:
                    traceability[artifact_id] = ['UNTRACED']
        
        return traceability
    
    def generate_traceability_matrix(self) -> Dict[str, List[str]]:
        """Generate traceability matrix from requirements to implementations"""
        matrix = {}
        
        for artifact_id, artifact in self.artifacts.items():
            if artifact_id.startswith('REQ-'):
                # Find all CODE/ARCH/API artifacts that reference this requirement
                related = []
                for other_id, other in self.artifacts.items():
                    related_ids = other.get('doc_tags', {}).get('related_artifacts', [])
                    if isinstance(related_ids, str):
                        related_ids = [related_ids]
                    
                    if artifact_id in related_ids:
                        related.append(other_id)
                
                matrix[artifact_id] = related
        
        return matrix


class LatexReferenceExtractor:
    """Extracts and validates LaTeX references"""
    
    @staticmethod
    def extract_ref_commands(latex_dir: Path) -> Dict[str, Tuple[str, int]]:
        """Extract all \\ref commands from LaTeX files with file/line info"""
        references = {}
        pattern = r'\\ref\{([^}]*)\}'
        
        for tex_file in latex_dir.glob('*.tex'):
            try:
                with open(tex_file, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        for match in re.finditer(pattern, line):
                            ref = match.group(1)
                            references[ref] = (str(tex_file), line_num)
            except UnicodeDecodeError:
                pass
        
        return references
    
    @staticmethod
    def extract_labels(latex_dir: Path) -> Dict[str, Tuple[str, int]]:
        """Extract all \\label commands from LaTeX files"""
        labels = {}
        pattern = r'\\label\{([^}]*)\}'
        
        for tex_file in latex_dir.glob('*.tex'):
            try:
                with open(tex_file, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        for match in re.finditer(pattern, line):
                            label = match.group(1)
                            labels[label] = (str(tex_file), line_num)
            except UnicodeDecodeError:
                pass
        
        return labels


def main():
    parser = argparse.ArgumentParser(
        description='Validate code-to-documentation mappings'
    )
    parser.add_argument('--metadata', type=Path, default=Path('./docs/code_metadata.json'),
                       help='Code metadata JSON file (from extract_code_docs.py)')
    parser.add_argument('--latex-dir', type=Path, default=Path('./Chapters'),
                       help='LaTeX chapters directory')
    parser.add_argument('--check-orphaned', action='store_true', default=True,
                       help='Check for orphaned code artifacts')
    parser.add_argument('--check-broken-refs', action='store_true', default=True,
                       help='Check for broken LaTeX references')
    parser.add_argument('--trace-design', action='store_true',
                       help='Trace design artifacts to requirements')
    parser.add_argument('--trace-to-requirements', type=str,
                       help='Trace specific prefix to requirements (e.g., ARCH, CODE)')
    parser.add_argument('--output', type=Path,
                       help='Output validation report (JSON)')
    
    args = parser.parse_args()
    
    # Initialize validator
    validator = MappingValidator()
    
    # Load metadata
    if not args.metadata.exists():
        print(f"Error: Metadata file not found: {args.metadata}")
        return
    
    validator.load_metadata(args.metadata)
    
    # Scan LaTeX references
    if not args.latex_dir.exists():
        print(f"Warning: LaTeX directory not found: {args.latex_dir}")
    else:
        validator.scan_latex_references(args.latex_dir)
    
    # Validate mappings
    print("\nValidating mappings...")
    results = validator.validate_mappings(
        check_orphaned=args.check_orphaned,
        check_broken=args.check_broken_refs
    )
    
    # Print statistics
    stats = validator.get_statistics()
    print(f"\nValidation Results:")
    print(f"  ✓ Valid mappings: {stats['valid']}")
    print(f"  ✗ Orphaned artifacts: {stats['orphaned']}")
    print(f"  ✗ Broken references: {stats['broken_refs']}")
    
    # Print details
    orphaned = [r for r in results if r.status == 'ORPHANED']
    if orphaned:
        print(f"\nOrphaned Code Artifacts (not referenced in LaTeX):")
        for result in orphaned[:10]:  # Show first 10
            print(f"  {result.artifact_id}: {result.file} (chapter: {result.chapter})")
        if len(orphaned) > 10:
            print(f"  ... and {len(orphaned) - 10} more")
    
    broken = [r for r in results if r.status == 'BROKEN_REF']
    if broken:
        print(f"\nBroken LaTeX References (no code artifact found):")
        for result in broken[:10]:  # Show first 10
            print(f"  {result.artifact_id}")
        if len(broken) > 10:
            print(f"  ... and {len(broken) - 10} more")
    
    # Traceability
    if args.trace_to_requirements:
        print(f"\nTraceability ({args.trace_to_requirements} → REQ):")
        traceability = validator.trace_to_requirements(args.trace_to_requirements)
        for artifact_id, reqs in list(traceability.items())[:5]:
            print(f"  {artifact_id} → {reqs}")
        if len(traceability) > 5:
            print(f"  ... and {len(traceability) - 5} more")
    
    # Save report
    if args.output:
        report = {
            'timestamp': str(Path.cwd()),
            'statistics': stats,
            'results': [
                {
                    'artifact_id': r.artifact_id,
                    'status': r.status,
                    'message': r.message,
                    'chapter': r.chapter,
                    'file': r.file
                }
                for r in results
            ]
        }
        
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✓ Report saved to {args.output}")


if __name__ == '__main__':
    main()
