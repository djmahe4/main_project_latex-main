#!/usr/bin/env python3
"""
Generate LaTeX Tables from Artifacts

Creates LaTeX table source code from extracted artifacts.
Generates requirement matrices, test case tables, API reference tables, etc.

Usage:
    python generate_tables.py --metadata docs/code_metadata.json --output-dir media/
    python generate_tables.py --by-type requirements,tests --format tabular
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict


class LaTeXTableGenerator:
    """Generates LaTeX tables from artifact metadata"""
    
    def __init__(self, metadata_file: Path):
        """Initialize with metadata"""
        self.artifacts: Dict[str, Dict] = {}
        self.load_metadata(metadata_file)
    
    def load_metadata(self, metadata_file: Path) -> None:
        """Load extracted artifact metadata"""
        with open(metadata_file) as f:
            data = json.load(f)
            for artifact in data.get('artifacts', []):
                self.artifacts[artifact['artifact_id']] = artifact
    
    def generate_requirement_table(self) -> str:
        """Generate requirements table"""
        reqs = [a for a in self.artifacts.values() if a['artifact_id'].startswith('REQ')]
        reqs.sort(key=lambda x: x['artifact_id'])
        
        latex = r"""\begin{table}[h]
  \centering
  \small
  \begin{tabular}{|l|p{6cm}|p{3cm}|l|}
    \hline
    \textbf{ID} & \textbf{Requirement} & \textbf{Priority} & \textbf{Status} \\
    \hline
"""
        
        for req in reqs:
            req_id = req['artifact_id']
            title = req['title'].replace('_', r'\_').replace('#', r'\#')
            priority = req['doc_tags'].get('priority', 'MEDIUM')
            status = req['doc_tags'].get('status', 'OPEN')
            
            latex += f"    {req_id} & {title} & {priority} & {status} \\\\\n"
            latex += "    \\hline\n"
        
        latex += r"""  \end{tabular}
  \caption{Functional Requirements}
  \label{tab:requirements}
\end{table}
"""
        
        return latex
    
    def generate_test_case_table(self) -> str:
        """Generate test cases table"""
        tests = [a for a in self.artifacts.values() if a['artifact_id'].startswith(('TC', 'TEST-SUITE'))]
        tests.sort(key=lambda x: x['artifact_id'])
        
        latex = r"""\begin{table}[h]
  \centering
  \small
  \begin{tabular}{|l|p{6cm}|l|}
    \hline
    \textbf{Test ID} & \textbf{Description} & \textbf{Pass Criteria} \\
    \hline
"""
        
        for test in tests:
            test_id = test['artifact_id']
            description = test['title'].replace('_', r'\_').replace('#', r'\#')
            pass_criteria = test['doc_tags'].get('pass_criteria', 'See test definition')[:50]
            
            latex += f"    {test_id} & {description} & {pass_criteria} \\\\\n"
            latex += "    \\hline\n"
        
        latex += r"""  \end{tabular}
  \caption{Test Cases}
  \label{tab:test_cases}
\end{table}
"""
        
        return latex
    
    def generate_api_reference_table(self) -> str:
        """Generate API reference table"""
        apis = [a for a in self.artifacts.values() if a['artifact_id'].startswith('API')]
        apis.sort(key=lambda x: x['artifact_id'])
        
        latex = r"""\begin{table}[h]
  \centering
  \small
  \begin{tabular}{|l|p{4cm}|p{4cm}|l|}
    \hline
    \textbf{Endpoint} & \textbf{Description} & \textbf{Parameters} & \textbf{Returns} \\
    \hline
"""
        
        for api in apis:
            api_id = api['artifact_id']
            description = api['title'].replace('_', r'\_').replace('#', r'\#')
            doc_tags = api['doc_tags']
            parameters = doc_tags.get('parameters', 'See documentation')[:30]
            returns = doc_tags.get('returns', 'See documentation')[:30]
            
            latex += f"    {api_id} & {description} & {parameters} & {returns} \\\\\n"
            latex += "    \\hline\n"
        
        latex += r"""  \end{tabular}
  \caption{API Reference}
  \label{tab:api_reference}
\end{table}
"""
        
        return latex
    
    def generate_performance_table(self) -> str:
        """Generate performance metrics table"""
        perf = [a for a in self.artifacts.values() 
                if a['artifact_id'].startswith(('PERF', 'METRIC'))]
        perf.sort(key=lambda x: x['artifact_id'])
        
        latex = r"""\begin{table}[h]
  \centering
  \small
  \begin{tabular}{|l|l|l|l|l|}
    \hline
    \textbf{Metric ID} & \textbf{Metric Name} & \textbf{Value} & \textbf{Threshold} & \textbf{Status} \\
    \hline
"""
        
        for metric in perf:
            metric_id = metric['artifact_id']
            metric_name = metric['title'].replace('_', r'\_')
            doc_tags = metric['doc_tags']
            value = doc_tags.get('value', 'N/A')
            threshold = doc_tags.get('threshold', 'N/A')
            status = doc_tags.get('status', 'PENDING')
            
            # Color code status
            if status == 'PASS':
                status_latex = r'\textcolor{green!60!black}{PASS}'
            elif status == 'FAIL':
                status_latex = r'\textcolor{red}{FAIL}'
            else:
                status_latex = status
            
            latex += f"    {metric_id} & {metric_name} & {value} & {threshold} & {status_latex} \\\\\n"
            latex += "    \\hline\n"
        
        latex += r"""  \end{tabular}
  \caption{Performance Metrics}
  \label{tab:performance}
\end{table}
"""
        
        return latex
    
    def generate_code_module_table(self) -> str:
        """Generate code modules reference table"""
        code = [a for a in self.artifacts.values() if a['artifact_id'].startswith('CODE')]
        code.sort(key=lambda x: x['artifact_id'])
        
        latex = r"""\begin{table}[h]
  \centering
  \small
  \begin{tabular}{|l|p{4cm}|p{3cm}|l|}
    \hline
    \textbf{Module ID} & \textbf{Description} & \textbf{Key Functions} & \textbf{Language} \\
    \hline
"""
        
        for module in code:
            mod_id = module['artifact_id']
            description = module['title'].replace('_', r'\_')[:40]
            doc_tags = module['doc_tags']
            key_functions = doc_tags.get('key_functions', 'See code')[:30]
            language = doc_tags.get('language', module['language']).upper()
            
            latex += f"    {mod_id} & {description} & {key_functions} & {language} \\\\\n"
            latex += "    \\hline\n"
        
        latex += r"""  \end{tabular}
  \caption{Code Modules}
  \label{tab:code_modules}
\end{table}
"""
        
        return latex
    
    def generate_traceability_matrix(self) -> str:
        """Generate traceability matrix (Requirements -> Implementation)"""
        # Group by requirement
        traceability = defaultdict(list)
        
        for artifact in self.artifacts.values():
            related = artifact['doc_tags'].get('related_artifacts', [])
            if isinstance(related, str):
                related = [related]
            
            for req_id in related:
                if req_id.startswith('REQ'):
                    traceability[req_id].append(artifact['artifact_id'])
        
        # Create matrix
        reqs = sorted([a for a in self.artifacts.values() if a['artifact_id'].startswith('REQ')],
                     key=lambda x: x['artifact_id'])
        
        if not reqs:
            return ""
        
        latex = r"""\begin{table}[h]
  \centering
  \small
  \begin{tabular}{|l|l|}
    \hline
    \textbf{Requirement} & \textbf{Implementations} \\
    \hline
"""
        
        for req in reqs:
            req_id = req['artifact_id']
            implementations = ', '.join(traceability.get(req_id, ['None']))[:60]
            
            latex += f"    {req_id} & {implementations} \\\\\n"
            latex += "    \\hline\n"
        
        latex += r"""  \end{tabular}
  \caption{Requirements Traceability Matrix}
  \label{tab:traceability}
\end{table}
"""
        
        return latex
    
    def generate_chapter_summary(self, chapter: str) -> str:
        """Generate summary table for a specific chapter"""
        artifacts_in_chapter = [
            a for a in self.artifacts.values()
            if a['chapter'].lower() == chapter.lower()
        ]

        # Group by type
        by_type = defaultdict(list)
        for artifact in artifacts_in_chapter:
            prefix = artifact['artifact_id'].split('-')[0]
            by_type[prefix].append(artifact)

        latex = r"""\begin{table}[h]
  \centering
  \small
  \begin{tabular}{|l|l|l|}
    \hline
    	extbf{Type} & \textbf{Count} & \textbf{Status} \\
    \hline
"""

        for artifact_type, artifacts in sorted(by_type.items()):
            count = len(artifacts)
            documented = len([a for a in artifacts if a['doc_tags'].get('description')])
            status = f"{documented}/{count}"

            latex += f"    {artifact_type} & {count} & {status} \\\\\n"
            latex += "    \\hline\n"

        latex += f"""  \\end{{tabular}}
  \caption{{Chapter: {chapter}}}
  \label{{tab:chapter_{chapter.lower().replace(' ', '_')}}}
\\end{{table}}
"""

        return latex
    
    def generate_all(self) -> Dict[str, str]:
        """Generate all standard tables"""
        return {
            'requirements': self.generate_requirement_table(),
            'test_cases': self.generate_test_case_table(),
            'api_reference': self.generate_api_reference_table(),
            'performance': self.generate_performance_table(),
            'code_modules': self.generate_code_module_table(),
            'traceability': self.generate_traceability_matrix(),
        }


def main():
    parser = argparse.ArgumentParser(
        description='Generate LaTeX tables from artifact metadata'
    )
    parser.add_argument('--metadata', type=Path, default=Path('./docs/code_metadata.json'),
                       help='Metadata JSON file')
    parser.add_argument('--output-dir', type=Path, default=Path('./media/tables'),
                       help='Output directory for LaTeX files')
    parser.add_argument('--by-type', type=str,
                       help='Specific table types (comma-separated: requirements,tests,api,performance,code,traceability)')
    parser.add_argument('--chapter', type=str,
                       help='Generate summary for specific chapter')
    parser.add_argument('--format', type=str, default='tabular',
                       help='Table format (tabular, tabulary, booktabs)')
    parser.add_argument('--single-file', action='store_true',
                       help='Combine all tables in single file')
    
    args = parser.parse_args()
    
    # Initialize generator
    if not args.metadata.exists():
        print(f"Error: Metadata file not found: {args.metadata}")
        return
    
    generator = LaTeXTableGenerator(args.metadata)
    
    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate tables
    if args.chapter:
        print(f"Generating summary for chapter: {args.chapter}")
        latex = generator.generate_chapter_summary(args.chapter)
        filename = f"chapter_summary_{args.chapter.lower().replace(' ', '_')}.tex"
        output_file = args.output_dir / filename
        with open(output_file, 'w') as f:
            f.write(latex)
        print(f"✓ Saved to {output_file}")
    else:
        tables = generator.generate_all()
        
        if args.by_type:
            types = args.by_type.split(',')
            tables = {k: v for k, v in tables.items() if k in types}
        
        if args.single_file:
            combined = '\n\n'.join(tables.values())
            output_file = args.output_dir / 'all_tables.tex'
            with open(output_file, 'w') as f:
                f.write(combined)
            print(f"✓ All tables saved to {output_file}")
        else:
            for table_type, latex_content in tables.items():
                if latex_content:
                    output_file = args.output_dir / f'{table_type}_table.tex'
                    with open(output_file, 'w') as f:
                        f.write(latex_content)
                    print(f"✓ {table_type} table saved to {output_file}")


if __name__ == '__main__':
    main()
