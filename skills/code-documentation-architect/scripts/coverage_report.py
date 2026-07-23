#!/usr/bin/env python3
"""
Coverage Report - Documentation Coverage Analysis

Generates comprehensive reports on documentation coverage of the codebase.
Shows what's documented, what's missing, and coverage metrics by chapter/component.

Usage:
    python coverage_report.py --metadata docs/code_metadata.json --output coverage.json
    python coverage_report.py --by-chapter --by-component
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict
from datetime import datetime


class CoverageAnalyzer:
    """Analyzes documentation coverage"""
    
    def __init__(self, metadata_file: Path):
        """Initialize with metadata"""
        self.artifacts: Dict[str, Dict] = {}
        self.load_metadata(metadata_file)
    
    def load_metadata(self, metadata_file: Path) -> None:
        """Load artifact metadata"""
        with open(metadata_file) as f:
            data = json.load(f)
            for artifact in data.get('artifacts', []):
                self.artifacts[artifact['artifact_id']] = artifact
    
    def calculate_overall_coverage(self) -> Dict:
        """Calculate overall documentation coverage"""
        total = len(self.artifacts)
        
        documented = len([a for a in self.artifacts.values() if a['doc_tags'].get('description')])
        
        with_examples = len([a for a in self.artifacts.values() 
                           if any(k in a['doc_tags'] for k in ['example', 'code_snippet'])])
        
        with_diagrams = len([a for a in self.artifacts.values() 
                            if 'diagram_id' in a['doc_tags']])
        
        return {
            'total_artifacts': total,
            'documented': documented,
            'coverage_percent': (documented / total * 100) if total > 0 else 0,
            'with_examples': with_examples,
            'with_diagrams': with_diagrams,
            'example_percent': (with_examples / total * 100) if total > 0 else 0,
        }
    
    def coverage_by_chapter(self) -> Dict[str, Dict]:
        """Analyze coverage by chapter"""
        by_chapter = defaultdict(list)
        
        for artifact in self.artifacts.values():
            chapter = artifact.get('chapter', 'UNKNOWN')
            by_chapter[chapter].append(artifact)
        
        results = {}
        for chapter, artifacts in by_chapter.items():
            total = len(artifacts)
            documented = len([a for a in artifacts if a['doc_tags'].get('description')])
            
            results[chapter] = {
                'total': total,
                'documented': documented,
                'undocumented': total - documented,
                'coverage_percent': (documented / total * 100) if total > 0 else 0,
                'artifacts': [a['artifact_id'] for a in artifacts]
            }
        
        return results
    
    def coverage_by_type(self) -> Dict[str, Dict]:
        """Analyze coverage by artifact type (REQ, CODE, API, etc.)"""
        by_type = defaultdict(list)
        
        for artifact in self.artifacts.values():
            artifact_type = artifact['artifact_id'].split('-')[0]
            by_type[artifact_type].append(artifact)
        
        results = {}
        for artifact_type, artifacts in by_type.items():
            total = len(artifacts)
            documented = len([a for a in artifacts if a['doc_tags'].get('description')])
            
            results[artifact_type] = {
                'total': total,
                'documented': documented,
                'undocumented': total - documented,
                'coverage_percent': (documented / total * 100) if total > 0 else 0,
                'artifact_ids': [a['artifact_id'] for a in artifacts]
            }
        
        return results
    
    def coverage_by_component(self) -> Dict[str, Dict]:
        """Analyze coverage by component (if tagged)"""
        by_component = defaultdict(list)
        
        for artifact in self.artifacts.values():
            component = artifact['doc_tags'].get('component', 'UNTAGGED')
            by_component[component].append(artifact)
        
        results = {}
        for component, artifacts in by_component.items():
            total = len(artifacts)
            documented = len([a for a in artifacts if a['doc_tags'].get('description')])
            
            results[component] = {
                'total': total,
                'documented': documented,
                'coverage_percent': (documented / total * 100) if total > 0 else 0,
            }
        
        return results
    
    def find_gaps(self) -> Dict[str, List[str]]:
        """Identify documentation gaps"""
        gaps = {
            'no_description': [],
            'no_examples': [],
            'no_diagrams': [],
            'no_tests': [],
            'broken_links': [],
        }
        
        for artifact_id, artifact in self.artifacts.items():
            doc_tags = artifact['doc_tags']
            
            if not doc_tags.get('description'):
                gaps['no_description'].append(artifact_id)
            
            if not any(k in doc_tags for k in ['example', 'code_snippet']):
                gaps['no_examples'].append(artifact_id)
            
            if artifact_id.startswith(('CODE', 'ARCH', 'SEQ', 'CLASS')):
                if 'diagram_id' not in doc_tags:
                    gaps['no_diagrams'].append(artifact_id)
            
            # Check for related_artifacts that don't exist
            related = doc_tags.get('related_artifacts', [])
            if isinstance(related, str):
                related = [related]
            
            for rel_id in related:
                if rel_id not in self.artifacts:
                    gaps['broken_links'].append(f"{artifact_id} → {rel_id}")
        
        return gaps
    
    def traceability_analysis(self) -> Dict:
        """Analyze requirements traceability"""
        requirements = [a for a in self.artifacts.values() 
                       if a['artifact_id'].startswith('REQ')]
        
        traced = 0
        untraced = 0
        
        for req in requirements:
            traced_items = []
            for artifact in self.artifacts.values():
                related = artifact['doc_tags'].get('related_artifacts', [])
                if isinstance(related, str):
                    related = [related]
                if req['artifact_id'] in related:
                    traced_items.append(artifact['artifact_id'])
            
            if traced_items:
                traced += 1
            else:
                untraced += 1
        
        return {
            'total_requirements': len(requirements),
            'traced': traced,
            'untraced': untraced,
            'traceability_percent': (traced / len(requirements) * 100) if requirements else 0,
        }
    
    def generate_full_report(self) -> Dict:
        """Generate comprehensive coverage report"""
        return {
            'timestamp': datetime.now().isoformat(),
            'overall': self.calculate_overall_coverage(),
            'by_chapter': self.coverage_by_chapter(),
            'by_type': self.coverage_by_type(),
            'by_component': self.coverage_by_component(),
            'gaps': self.find_gaps(),
            'traceability': self.traceability_analysis(),
        }


def print_report_summary(report: Dict) -> None:
    """Print a human-readable summary of the coverage report"""
    overall = report['overall']
    
    print("\n" + "="*60)
    print("DOCUMENTATION COVERAGE REPORT")
    print("="*60)
    
    print(f"\nOverall Coverage:")
    print(f"  Total Artifacts: {overall['total_artifacts']}")
    print(f"  Documented: {overall['documented']}")
    print(f"  Coverage: {overall['coverage_percent']:.1f}%")
    print(f"  With Examples: {overall['with_examples']} ({overall['example_percent']:.1f}%)")
    print(f"  With Diagrams: {overall['with_diagrams']}")
    
    # Coverage by type
    print(f"\nCoverage by Artifact Type:")
    by_type = report['by_type']
    for atype in sorted(by_type.keys()):
        info = by_type[atype]
        bar = '█' * int(info['coverage_percent'] / 5) + '░' * (20 - int(info['coverage_percent'] / 5))
        print(f"  {atype:12} [{bar}] {info['coverage_percent']:5.1f}% ({info['documented']}/{info['total']})")
    
    # Coverage by chapter
    print(f"\nCoverage by Chapter:")
    by_chapter = report['by_chapter']
    for chapter in sorted(by_chapter.keys()):
        info = by_chapter[chapter]
        bar = '█' * int(info['coverage_percent'] / 5) + '░' * (20 - int(info['coverage_percent'] / 5))
        print(f"  {chapter:20} [{bar}] {info['coverage_percent']:5.1f}% ({info['documented']}/{info['total']})")
    
    # Traceability
    trace = report['traceability']
    print(f"\nRequirements Traceability:")
    print(f"  Total Requirements: {trace['total_requirements']}")
    print(f"  Traced: {trace['traced']}")
    print(f"  Untraced: {trace['untraced']}")
    print(f"  Traceability: {trace['traceability_percent']:.1f}%")
    
    # Gaps
    gaps = report['gaps']
    print(f"\nDocumentation Gaps:")
    if gaps['no_description']:
        print(f"  No description: {len(gaps['no_description'])} artifacts")
        for aid in gaps['no_description'][:5]:
            print(f"    - {aid}")
        if len(gaps['no_description']) > 5:
            print(f"    ... and {len(gaps['no_description']) - 5} more")
    
    if gaps['broken_links']:
        print(f"  Broken references: {len(gaps['broken_links'])}")
        for link in gaps['broken_links'][:5]:
            print(f"    - {link}")
        if len(gaps['broken_links']) > 5:
            print(f"    ... and {len(gaps['broken_links']) - 5} more")
    
    print("\n" + "="*60)


def main():
    parser = argparse.ArgumentParser(
        description='Generate documentation coverage report'
    )
    parser.add_argument('--metadata', type=Path, default=Path('./docs/code_metadata.json'),
                       help='Metadata JSON file')
    parser.add_argument('--output', type=Path,
                       help='Output report file (JSON)')
    parser.add_argument('--by-chapter', action='store_true',
                       help='Show coverage breakdown by chapter')
    parser.add_argument('--by-type', action='store_true',
                       help='Show coverage breakdown by artifact type')
    parser.add_argument('--by-component', action='store_true',
                       help='Show coverage breakdown by component')
    parser.add_argument('--show-gaps', action='store_true',
                       help='Show detailed documentation gaps')
    parser.add_argument('--traceability', action='store_true',
                       help='Show requirements traceability analysis')
    parser.add_argument('--html', type=Path,
                       help='Generate HTML report')
    
    args = parser.parse_args()
    
    # Initialize analyzer
    if not args.metadata.exists():
        print(f"Error: Metadata file not found: {args.metadata}")
        return
    
    analyzer = CoverageAnalyzer(args.metadata)
    report = analyzer.generate_full_report()
    
    # Print summary
    print_report_summary(report)
    
    # Save JSON report
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n✓ Detailed report saved to {args.output}")
    
    # Generate HTML report
    if args.html:
        html_report = generate_html_report(report)
        with open(args.html, 'w') as f:
            f.write(html_report)
        print(f"✓ HTML report saved to {args.html}")


def generate_html_report(report: Dict) -> str:
    """Generate an HTML version of the coverage report"""
    overall = report['overall']
    by_type = report['by_type']
    
    html = """<!DOCTYPE html>
<html>
<head>
    <title>Documentation Coverage Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        .metric { display: inline-block; margin: 10px; padding: 10px; border: 1px solid #ddd; }
        .progress { background: #eee; border-radius: 5px; overflow: hidden; }
        .progress-bar { background: #4CAF50; height: 20px; display: flex; align-items: center; justify-content: center; color: white; font-size: 12px; }
        table { border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background: #f0f0f0; }
    </style>
</head>
<body>
    <h1>Documentation Coverage Report</h1>
"""
    
    html += f"""
    <div class="metric">
        <strong>Overall Coverage:</strong><br/>
        <div class="progress" style="width: 200px;">
            <div class="progress-bar" style="width: {overall['coverage_percent']}%;">
                {overall['coverage_percent']:.1f}%
            </div>
        </div>
    </div>
    <div class="metric">
        <strong>Artifacts:</strong> {overall['total_artifacts']}<br/>
        <strong>Documented:</strong> {overall['documented']}
    </div>
"""
    
    html += """
    <h2>Coverage by Type</h2>
    <table>
        <tr><th>Type</th><th>Total</th><th>Documented</th><th>Coverage</th></tr>
"""
    
    for atype in sorted(by_type.keys()):
        info = by_type[atype]
        html += f"""        <tr>
            <td>{atype}</td>
            <td>{info['total']}</td>
            <td>{info['documented']}</td>
            <td>
                <div class="progress" style="width: 150px;">
                    <div class="progress-bar" style="width: {info['coverage_percent']}%;">
                        {info['coverage_percent']:.1f}%
                    </div>
                </div>
            </td>
        </tr>
"""
    
    html += """
    </table>
    </body>
</html>
"""
    
    return html


if __name__ == '__main__':
    main()
